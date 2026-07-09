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
# Noise Removal (FFmpeg)
# -------------------------------------------------

def remove_noise():
    (
        ffmpeg
        .input("video.mp4")
        .output(
            "static/outputs/output.mp4",
            af="afftdn"
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

def create_noise_reduced_video(url: str):
    download_video(url)

    remove_noise()

    cleanup()

    return "static/outputs/output.mp4"