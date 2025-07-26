import os
import yt_dlp

VIDEO_DIR = "videos"
os.makedirs(VIDEO_DIR, exist_ok=True)

video_urls = [
    "https://youtu.be/k0Ka-deab1s",
    "https://youtu.be/fezKpDFKf5U",
    "https://youtu.be/76RnAYrx2Ik",
    "https://youtu.be/DCQHfrqMKXA",
    "https://youtu.be/Rz6__sLHPNA",
    "https://youtu.be/8lD5bfqzr6E",
    "https://youtu.be/cen1SvpTsYk"
]

# Download videos
for idx, url in enumerate(video_urls, start=1):
    try:
        video_filename = os.path.join(VIDEO_DIR, f"video{idx}.mp4")
        ydl_opts = {
            "format": "best",
            "outtmpl": video_filename,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"✅ Downloaded: video{idx}.mp4")

    except Exception as e:
        print(f"❌ Failed to download {url}: {e}")
