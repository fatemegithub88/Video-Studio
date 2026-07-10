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
# # Boost Audio Volume
# # -------------------------------------------------

# def boost_audio(volume: float = 1.5):
#     """
#     volume:
#         1.0 = normal
#         1.5 = +50%
#         2.0 = loud
#     """

#     (
#         ffmpeg
#         .input("video.mp4")
#         .output(
#             "static/outputs/output.mp4",
#             af=f"volume={volume}"
#         )
#         .run(overwrite_output=True)
#     )

# # -------------------------------------------------
# # Cleanup
# # -------------------------------------------------

# def cleanup():
#     if os.path.exists("video.mp4"):
#         os.remove("video.mp4")


# # -------------------------------------------------
# # Main Pipeline
# # -------------------------------------------------

# def create_boosted_video(url: str, volume: float = 1.5):

#     download_video(url)

#     boost_audio(volume)

#     cleanup()

#     return "static/outputs/output.mp4"


import os
import uuid
import yt_dlp
import ffmpeg

# -------------------------------------------------
# Download Video
# -------------------------------------------------

def download_video(link):

    uid = uuid.uuid4().hex

    video_file = f"temp/{uid}.%(ext)s"

    ydl_opts = {
        "format": "best",
        "outtmpl": video_file
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])

    base = video_file.replace(".%(ext)s", "")

    for file in os.listdir("temp"):
        if file.startswith(uid):
            return os.path.join("temp", file), uid

    raise FileNotFoundError("Downloaded video not found.")


# -------------------------------------------------
# Boost Audio Volume
# -------------------------------------------------

def boost_audio(input_file, output_file, volume=1.5):

    (
        ffmpeg
        .input(input_file)
        .output(
            output_file,
            af=f"volume={volume}"
        )
        .run(overwrite_output=True)
    )


# -------------------------------------------------
# Cleanup
# -------------------------------------------------

def cleanup(file_path):

    if os.path.exists(file_path):
        os.remove(file_path)


# -------------------------------------------------
# Main Pipeline
# -------------------------------------------------

def create_boosted_video(url: str, volume: float = 1.5):

    video_file, uid = download_video(url)

    output_file = f"static/outputs/{uid}.mp4"

    boost_audio(
        video_file,
        output_file,
        volume
    )

    cleanup(video_file)

    return output_file