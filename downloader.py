# downloader.py

import subprocess
import uuid
import os

DOWNLOAD_DIR = "downloads"
COOKIES_PATH = "/tmp/instagram_cookies.txt"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def download_instagram_audio(url: str, audio_format: str = "mp3") -> str:
    """
    Downloads audio from an Instagram permalink using yt-dlp.
    Returns path to audio file.
    """

    filename = f"{uuid.uuid4()}.{audio_format}"
    filepath = os.path.join(DOWNLOAD_DIR, filename)

    cmd = [
        "yt-dlp",
        "-f", "bestaudio",
        "--extract-audio",
        "--audio-format", audio_format,
        "--audio-quality", "0",
        "--extractor-args", "instagram:app=android",
        "--no-check-certificates",
        "--user-agent", "Mozilla/5.0 (Linux; Android 11; SM-G991B)",
        "-o", filepath,
        url
    ]
    # Inject cookies only if the file exists (avoids hard crash on fresh deploys)
    if os.path.exists(COOKIES_PATH):
        cmd[1:1] = ["--cookies", COOKIES_PATH]

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        raise Exception(f"yt-dlp failed: {result.stderr.decode()[-300:]}")

    return filepath
