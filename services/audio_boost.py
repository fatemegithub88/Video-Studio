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
# Boost Audio Volume
# -------------------------------------------------

def boost_audio(volume: float = 1.5):
    """
    volume:
        1.0 = normal
        1.5 = +50%
        2.0 = loud
    """

    (
        ffmpeg
        .input("video.mp4")
        .output(
            "static/outputs/output.mp4",
            af=f"volume={volume}"
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

def create_boosted_video(url: str, volume: float = 1.5):

    download_video(url)

    boost_audio(volume)

    cleanup()

    return "static/outputs/output.mp4"