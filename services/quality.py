# import yt_dlp
# import ffmpeg
# import os

# # -------------------------------------------------
# # Download Video
# # -------------------------------------------------

# def download_video(link):

#     ydl_opts = {
#         "format": "best",
#         "outtmpl": "video.%(ext)s"
#     }

#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([link])


# # -------------------------------------------------
# # Convert Quality
# # -------------------------------------------------

# def convert_quality(quality):

#     quality_map = {
#         "1080p": "1920:1080",
#         "720p": "1280:720",
#         "480p": "854:480",
#         "360p": "640:360",
#         "144p": "256:144"
#     }

#     scale = quality_map[quality]

#     ffmpeg.input("video.mp4").output(
#         "static/outputs/output.mp4",
#         vf=f"scale={scale}"
#     ).run(overwrite_output=True)


# # -------------------------------------------------
# # Cleanup
# # -------------------------------------------------

# def cleanup():
#     os.remove("video.mp4")


# # -------------------------------------------------
# # Main Pipeline
# # -------------------------------------------------

# def create_quality_video(url: str, quality: str):

#     download_video(url)

#     convert_quality(quality)

#     cleanup()

#     return "static/outputs/output.mp4"


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
# Convert Quality
# -------------------------------------------------

def convert_quality(quality):

    quality_map = {
        "1080p": "1920:1080",
        "720p": "1280:720",
        "480p": "854:480",
        "360p": "640:360",
        "144p": "256:144"
    }

    scale = quality_map[quality]

    stream = (
        ffmpeg
        .input("video.mp4")
        .output(
            "static/outputs/output.mp4",
            vf=f"scale={scale}"
        )
    )

    print("\n========== FFMPEG COMMAND ==========")
    print(" ".join(ffmpeg.compile(stream)))
    print("====================================\n")

    try:
        stream.run(
            overwrite_output=True,
            capture_stdout=True,
            capture_stderr=True
        )

    except ffmpeg.Error as e:

        print("\n========== FFMPEG STDERR ==========")

        if e.stderr:
            print(e.stderr.decode("utf-8", errors="ignore"))

        print("===================================\n")

        raise


# -------------------------------------------------
# Cleanup
# -------------------------------------------------

def cleanup():

    if os.path.exists("video.mp4"):
        os.remove("video.mp4")


# -------------------------------------------------
# Main Pipeline
# -------------------------------------------------

def create_quality_video(url: str, quality: str):

    download_video(url)

    convert_quality(quality)

    cleanup()

    return "static/outputs/output.mp4"