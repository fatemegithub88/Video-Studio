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
# Build Audio Speed Filter
# -------------------------------------------------

def build_atempo(speed: float) -> str:
    """
    FFmpeg atempo only supports values between 0.5 and 2.0.
    This function creates a valid filter chain.
    """

    filters = []

    while speed > 2:
        filters.append("atempo=2")
        speed /= 2

    while speed < 0.5:
        filters.append("atempo=0.5")
        speed *= 2

    filters.append(f"atempo={speed:.3f}")

    return ",".join(filters)


# -------------------------------------------------
# Change Speed
# -------------------------------------------------

def change_speed(speed: float):

    video_filter = f"setpts={1/speed}*PTS"

    audio_filter = build_atempo(speed)

    (
        ffmpeg
        .input("video.mp4")
        .output(
            "static/outputs/output.mp4",
            vf=video_filter,
            af=audio_filter
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

def create_speed_video(url: str, speed: float):

    download_video(url)

    change_speed(speed)

    cleanup()

    return "static/outputs/output.mp4"