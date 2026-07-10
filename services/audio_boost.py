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


# import os
# import uuid
# import yt_dlp
# import ffmpeg

# # -------------------------------------------------
# # Download Video
# # -------------------------------------------------

# def download_video(link):

#     uid = uuid.uuid4().hex

#     video_file = f"temp/{uid}.%(ext)s"

#     ydl_opts = {
#         "format": "best",
#         "outtmpl": video_file
#     }

#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([link])

#     base = video_file.replace(".%(ext)s", "")

#     for file in os.listdir("temp"):
#         if file.startswith(uid):
#             return os.path.join("temp", file), uid

#     raise FileNotFoundError("Downloaded video not found.")


# # -------------------------------------------------
# # Boost Audio Volume
# # -------------------------------------------------

# def boost_audio(input_file, output_file, volume=1.5):

#     (
#         ffmpeg
#         .input(input_file)
#         .output(
#             output_file,
#             af=f"volume={volume}"
#         )
#         .run(overwrite_output=True)
#     )


# # -------------------------------------------------
# # Cleanup
# # -------------------------------------------------

# def cleanup(file_path):

#     if os.path.exists(file_path):
#         os.remove(file_path)


# # -------------------------------------------------
# # Main Pipeline
# # -------------------------------------------------

# def create_boosted_video(url: str, volume: float = 1.5):

#     video_file, uid = download_video(url)

#     output_file = f"static/outputs/{uid}.mp4"

#     boost_audio(
#         video_file,
#         output_file,
#         volume
#     )

#     cleanup(video_file)

#     return output_file

import os
import uuid
import subprocess
import yt_dlp


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

    output_template = os.path.join(
        TEMP_DIR,
        f"{uid}.%(ext)s"
    )


    ydl_opts = {

        "format":
        "bestvideo[height<=720]+bestaudio/best",

        "outtmpl":
        output_template,

        "merge_output_format":
        "mp4",

        "noplaylist":
        True,

        "quiet":
        True
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
        "Downloaded video not found"
    )



# -------------------------------------------------
# Boost Audio Volume
# -------------------------------------------------

def boost_audio(
    input_file,
    output_file,
    volume=1.5
):


    command = [

        "ffmpeg",

        "-y",

        "-i",
        input_file,


        # audio filter
        "-af",
        f"volume={volume}",


        # video copy
        "-c:v",
        "copy",


        # audio encode
        "-c:a",
        "aac",

        "-b:a",
        "192k",


        "-movflags",
        "+faststart",


        output_file
    ]



    result = subprocess.run(

        command,

        stdout=subprocess.DEVNULL,

        stderr=subprocess.PIPE,

        text=True

    )



    if result.returncode != 0:

        raise Exception(
            f"FFmpeg Error:\n{result.stderr}"
        )



    if not os.path.exists(output_file):

        raise Exception(
            "Output video was not created"
        )



# -------------------------------------------------
# Cleanup
# -------------------------------------------------

def cleanup(file_path):

    try:

        if file_path and os.path.exists(file_path):

            os.remove(file_path)

    except:

        pass



# -------------------------------------------------
# Main Pipeline
# -------------------------------------------------

def create_boosted_video(
    url: str,
    volume: float = 1.5
):


    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )


    video_file = None


    uid = uuid.uuid4().hex


    output_file = os.path.join(
        OUTPUT_DIR,
        f"{uid}.mp4"
    )



    try:


        video_file = download_video(
            url
        )


        boost_audio(

            video_file,

            output_file,

            volume

        )


        return output_file



    finally:


        cleanup(
            video_file
        )