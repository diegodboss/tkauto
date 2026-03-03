import json
import os
from nicetker import SuchuangClient


token = os.getenv("SUCHUANG_TOKEN")
base_url = os.getenv("SUCHUANG_BASE_URL", "https://t.51suchuang.com")

title = "Test Video"
post_time = "2026-03-01 12:00:00"
timezone = "Asia/Shanghai"
video_path = "/path/to/test.mp4"


if not token:
    raise SystemExit("Missing SUCHUANG_TOKEN")

client = SuchuangClient(token=token, base_url=base_url)
resp = client.publish_video(
    title=title,
    post_time=post_time,
    timezone=timezone,
    video_path=video_path,
)

if isinstance(resp, (dict, list)):
    print(json.dumps(resp, ensure_ascii=False, indent=2))
else:
    print(resp)
