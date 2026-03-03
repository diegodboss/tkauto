from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional, Union

import requests


class SuchuangAPIError(RuntimeError):
    def __init__(self, message: str, *, status_code: Optional[int] = None, payload: Any = None):
        super().__init__(message)
        self.status_code = status_code
        self.payload = payload


@dataclass
class SuchuangClient:
    token: str
    base_url: str = "https://t.51suchuang.com"
    timeout: Union[float, tuple[float, float]] = 30.0

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
        }

    def publish_video(
        self,
        *,
        title: str,
        post_time: str,
        timezone: str,
        video_path: Union[str, Path],
        extra_fields: Optional[Dict[str, str]] = None,
    ) -> Any:
        """Publish a video via /api/video/publish.

        Args:
            title: Video title.
            post_time: e.g. "2026-03-01 12:00:00".
            timezone: e.g. "Asia/Shanghai".
            video_path: Path to local video file.
            extra_fields: Any additional form fields required by the API.

        Returns:
            Parsed JSON if response is JSON, otherwise raw text.

        Raises:
            FileNotFoundError: If video_path does not exist.
            SuchuangAPIError: On HTTP error or non-2xx response.
        """

        path = Path(video_path)
        if not path.exists() or not path.is_file():
            raise FileNotFoundError(f"video file not found: {path}")

        url = f"{self.base_url.rstrip('/')}/api/video/publish"

        data: Dict[str, str] = {
            "title": title,
            "post_time": post_time,
            "timezone": timezone,
        }
        if extra_fields:
            data.update(extra_fields)

        with path.open("rb") as f:
            files = {
                "video": (path.name, f, "application/octet-stream"),
            }
            try:
                r = requests.post(
                    url,
                    headers=self._headers(),
                    data=data,
                    files=files,
                    timeout=self.timeout,
                )
            except requests.RequestException as e:
                raise SuchuangAPIError(f"request failed: {e}") from e

        if not (200 <= r.status_code < 300):
            payload: Any
            try:
                payload = r.json()
            except ValueError:
                payload = r.text
            raise SuchuangAPIError(
                f"publish failed with status {r.status_code}",
                status_code=r.status_code,
                payload=payload,
            )

        content_type = r.headers.get("Content-Type", "")
        if "application/json" in content_type:
            return r.json()
        return r.text
