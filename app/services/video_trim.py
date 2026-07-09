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
# Trim Video (Cut)
# -------------------------------------------------

def trim_video(start: int, end: int):
    (
        ffmpeg
        .input("video.mp4", ss=start, to=end)
        .output(
            "static/outputs/output.mp4",
            c="copy" 
        )
        .run(overwrite_output=True)
    )


# -------------------------------------------------
# Cleanup
# -------------------------------------------------

def cleanup():
    if os.path.exists("video.mp4"):
        os.remove("video.mp4")


# -------------------------------------------------
# Main Pipeline
# -------------------------------------------------

def create_trimmed_video(url: str, start: int, end: int):

    download_video(url)

    trim_video(start, end)

    cleanup()

    return "static/outputs/output.mp4"