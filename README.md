# nicetker

简单又好用的tiktok图文、视频发布接口，功能强大，不需要魔法。agent轻松引用

## Features

- Publish video via `POST /api/video/publish`
- `multipart/form-data` upload
- Bearer Token auth
- Basic error handling

## Requirements

- Python >= 3.9
- `requests`

## Install

### Install from source (editable)

```bash
pip install -e .
```

### Build & install wheel (offline)

Build:

```bash
python -m pip install --upgrade build
python -m build
```

Install:

```bash
pip install dist/nicetker-0.1.0-py3-none-any.whl
```

## Quickstart

```python
from nicetker import SuchuangClient

client = SuchuangClient(token="YOUR_TOKEN")

resp = client.publish_video(
    title="Test Video",
    post_time="2026-03-01 12:00:00",
    timezone="Asia/Shanghai",
    video_path="/path/to/test.mp4",
)

print(resp)
```

## Demo

This repo includes a minimal runnable demo: `demo.py`.

```bash
export SUCHUANG_TOKEN="YOUR_TOKEN"
python demo.py
```

Edit variables in `demo.py` to change `title/post_time/timezone/video_path`.

## API

### `SuchuangClient`

```python
SuchuangClient(
    token: str,
    base_url: str = "https://t.51suchuang.com",
    timeout: float | tuple = 30.0,
)
```

### `publish_video`

```python
publish_video(
    *,
    title: str,
    post_time: str,
    timezone: str,
    video_path: str | Path,
    extra_fields: dict[str, str] | None = None,
)
```

## Token

token获取网址：https://t.51suchuang.com

## Contact

如遇到问题可联系作者QQ：285952371
