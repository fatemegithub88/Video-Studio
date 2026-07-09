import yt_dlp
import ffmpeg
import os

# -------------------------------------------------
# Download Video
# -------------------------------------------------

def download_video(link):

    ydl_opts = {
        "format": "best",
        "outtmpl": "video.%(ext)s"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])


# -------------------------------------------------
# Compress Video
# -------------------------------------------------

def compress_video(level):

    crf_map = {
        "low": 18,
        "medium": 28,
        "high": 35
    }

    crf = crf_map[level]

    ffmpeg.input("video.mp4").output(
        "static/outputs/output.mp4",
        vcodec="libx264",
        crf=crf,
        preset="medium"
    ).run(overwrite_output=True)


# -------------------------------------------------
# Cleanup
# -------------------------------------------------

def cleanup():

    os.remove("video.mp4")


# -------------------------------------------------
# Main Pipeline
# -------------------------------------------------

def create_compressed_video(url: str, level: str):

    download_video(url)

    compress_video(level)

    cleanup()

    return "static/outputs/output.mp4"