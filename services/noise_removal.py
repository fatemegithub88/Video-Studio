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
# # Noise Removal (FFmpeg)
# # -------------------------------------------------

# def remove_noise():
#     (
#         ffmpeg
#         .input("video.mp4")
#         .output(
#             "static/outputs/output.mp4",
#             af="afftdn"
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

# def create_noise_reduced_video(url: str):
#     download_video(url)

#     remove_noise()

#     cleanup()

#     return "static/outputs/output.mp4"


import os
import uuid
import yt_dlp
import ffmpeg


# -------------------------------------------------
# Directories
# -------------------------------------------------

OUTPUT_DIR = "static/outputs"
TEMP_DIR = "temp"


# -------------------------------------------------
# Download Video
# -------------------------------------------------

def download_video(link):

    os.makedirs(
        TEMP_DIR,
        exist_ok=True
    )


    uid = uuid.uuid4().hex

    temp_file = f"{TEMP_DIR}/{uid}.%(ext)s"


    ydl_opts = {

        "format": "best",

        "outtmpl": temp_file
    }


    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])


    for file in os.listdir(TEMP_DIR):

        if file.startswith(uid):

            return os.path.join(
                TEMP_DIR,
                file
            )


    raise FileNotFoundError(
        "Downloaded video not found."
    )


# -------------------------------------------------
# Noise Removal (FFmpeg)
# -------------------------------------------------

def remove_noise(
    input_file,
    output_file
):

    (
        ffmpeg
        .input(input_file)
        .output(
            output_file,
            af="afftdn"
        )
        .run(
            overwrite_output=True
        )
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

def create_noise_reduced_video(url: str):


    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )


    video_file = download_video(url)


    uid = uuid.uuid4().hex

    output_file = (
        f"{OUTPUT_DIR}/{uid}.mp4"
    )


    remove_noise(
        video_file,
        output_file
    )


    cleanup(video_file)


    return output_file