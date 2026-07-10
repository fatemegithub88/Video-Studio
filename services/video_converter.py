# import yt_dlp
# import ffmpeg
# import os

# OUTPUT_DIR = "static/outputs"

# # -------------------------------------------------
# # Download Video (any format)
# # -------------------------------------------------

# def download_video(link):

#     ydl_opts = {
#         "format": "bestvideo+bestaudio/best",
#         "merge_output_format": "mp4",
#         "outtmpl": "video.%(ext)s"
#     }

#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([link])


# # -------------------------------------------------
# # Convert Format
# # -------------------------------------------------

# def convert_format(output_format: str):

#     """
#     output_format:
#     mp4 | mkv | webm | mov
#     """

#     os.makedirs(OUTPUT_DIR, exist_ok=True)

#     output_file = os.path.join(
#         OUTPUT_DIR,
#         f"output.{output_format}"
#     )

#     (
#         ffmpeg
#         .input("video.mp4")
#         .output(
#             output_file,
#             vcodec="libx264",
#             acodec="aac"
#         )
#         .run(overwrite_output=True)
#     )

#     return output_file


# # -------------------------------------------------
# # Cleanup
# # -------------------------------------------------

# def cleanup():

#     if os.path.exists("video.mp4"):
#         os.remove("video.mp4")


# # -------------------------------------------------
# # Main Pipeline
# # -------------------------------------------------

# def create_converted_video(url: str, output_format: str):

#     download_video(url)

#     output_path = convert_format(output_format)

#     cleanup()

#     return output_path


# import os
# import uuid
# import yt_dlp
# import ffmpeg


# # -------------------------------------------------
# # Directories
# # -------------------------------------------------

# OUTPUT_DIR = "static/outputs"
# TEMP_DIR = "temp"


# # -------------------------------------------------
# # Download Video (any format)
# # -------------------------------------------------

# def download_video(link):


#     os.makedirs(
#         TEMP_DIR,
#         exist_ok=True
#     )


#     uid = uuid.uuid4().hex


#     temp_file = (
#         f"{TEMP_DIR}/{uid}.%(ext)s"
#     )


#     ydl_opts = {

#         "format": "bestvideo+bestaudio/best",

#         "merge_output_format": "mp4",

#         "outtmpl": temp_file
#     }


#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:

#         ydl.download([link])


#     for file in os.listdir(TEMP_DIR):

#         if file.startswith(uid):

#             return os.path.join(
#                 TEMP_DIR,
#                 file
#             )


#     raise FileNotFoundError(
#         "Downloaded video not found."
#     )



# # -------------------------------------------------
# # Convert Format
# # -------------------------------------------------

# def convert_format(
#     input_file,
#     output_file,
#     output_format: str
# ):

#     """
#     output_format:
#     mp4 | mkv | webm | mov
#     """


#     (
#         ffmpeg
#         .input(input_file)
#         .output(
#             output_file,
#             vcodec="libx264",
#             acodec="aac"
#         )
#         .run(
#             overwrite_output=True
#         )
#     )


#     return output_file



# # -------------------------------------------------
# # Cleanup
# # -------------------------------------------------

# def cleanup(file_path):


#     if os.path.exists(file_path):

#         os.remove(file_path)



# # -------------------------------------------------
# # Main Pipeline
# # -------------------------------------------------

# def create_converted_video(
#     url: str,
#     output_format: str
# ):


#     os.makedirs(
#         OUTPUT_DIR,
#         exist_ok=True
#     )


#     video_file = download_video(
#         url
#     )


#     uid = uuid.uuid4().hex


#     output_file = (
#         f"{OUTPUT_DIR}/{uid}.{output_format}"
#     )


#     convert_format(
#         video_file,
#         output_file,
#         output_format
#     )


#     cleanup(
#         video_file
#     )


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

def download_video(url):

    os.makedirs(
        TEMP_DIR,
        exist_ok=True
    )


    uid = uuid.uuid4().hex


    output_template = os.path.join(
        TEMP_DIR,
        f"{uid}.%(ext)s"
    )


    options = {

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



    with yt_dlp.YoutubeDL(options) as ydl:

        ydl.download([url])



    for file in os.listdir(TEMP_DIR):

        if file.startswith(uid):

            return os.path.join(
                TEMP_DIR,
                file
            )


    raise FileNotFoundError(
        "Download failed"
    )




# -------------------------------------------------
# Convert Format
# -------------------------------------------------

def convert_format(
    input_file,
    output_file,
    output_format
):


    output_format = output_format.lower()



    supported = [

        "mp4",
        "mkv",
        "mov",
        "webm"

    ]


    if output_format not in supported:

        output_format = "mp4"



    if output_format == "webm":

        video_codec = "libvpx-vp9"
        audio_codec = "libopus"


    else:

        video_codec = "libx264"
        audio_codec = "aac"



    command = [

        "ffmpeg",

        "-y",

        "-i",
        input_file,


        "-c:v",
        video_codec,


        "-c:a",
        audio_codec,


        "-preset",
        "veryfast",


        "-crf",
        "23",


        "-pix_fmt",
        "yuv420p",


        "-b:a",
        "128k",


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

            "FFmpeg conversion failed:\n"
            + result.stderr[-3000:]

        )



    if not os.path.exists(output_file):

        raise Exception(
            "Output file was not created"
        )



    return output_file





# -------------------------------------------------
# Cleanup
# -------------------------------------------------

def cleanup(path):

    try:

        if path and os.path.exists(path):

            os.remove(path)

    except:

        pass





# -------------------------------------------------
# Main Pipeline
# -------------------------------------------------

def create_converted_video(
    url: str,
    output_format: str
):


    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )


    source = None



    uid = uuid.uuid4().hex



    output_file = os.path.join(

        OUTPUT_DIR,

        f"{uid}.{output_format}"

    )



    try:


        source = download_video(
            url
        )


        convert_format(

            source,

            output_file,

            output_format

        )



        return output_file



    finally:


        cleanup(
            source
        )