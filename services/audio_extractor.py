# # import yt_dlp

# # # ---------------------------------
# # # Extract Audio (with format support)
# # # ---------------------------------

# # def extract_audio(link: str, format_type: str = "mp3"):

# #     allowed_formats = ["mp3", "wav", "m4a", "opus"]

# #     if format_type not in allowed_formats:
# #         format_type = "mp3"

# #     ydl_opts = {
# #         "format": "bestaudio/best",
# #         "outtmpl": "audio_of_video.%(ext)s",
# #         "postprocessors": [{
# #             "key": "FFmpegExtractAudio",
# #             "preferredcodec": format_type,
# #             "preferredquality": "192",
# #         }],
# #     }

# #     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
# #         ydl.download([link])

# #     return f"audio_of_video.{format_type}"


# import os
# import yt_dlp

# OUTPUT_DIR = "static/outputs"

# # ---------------------------------
# # Extract Audio (with format support)
# # ---------------------------------

# def extract_audio(link: str, format_type: str = "mp3"):

#     os.makedirs(OUTPUT_DIR, exist_ok=True)

#     allowed_formats = ["mp3", "wav", "m4a", "opus"]

#     if format_type not in allowed_formats:
#         format_type = "mp3"

#     output_name = os.path.join(OUTPUT_DIR, "audio")

#     ydl_opts = {
#         "format": "bestaudio/best",
#         "outtmpl": output_name + ".%(ext)s",
#         "postprocessors": [{
#             "key": "FFmpegExtractAudio",
#             "preferredcodec": format_type,
#             "preferredquality": "192",
#         }],
#     }

#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([link])

#     return f"{output_name}.{format_type}"


# import os
# import uuid
# import yt_dlp

# # -------------------------------------------------
# # Extract Audio
# # -------------------------------------------------

# OUTPUT_DIR = "static/outputs"
# TEMP_DIR = "temp"


# # -------------------------------------------------
# # Download & Extract Audio
# # -------------------------------------------------

# def extract_audio(link: str, format_type: str = "mp3"):

#     os.makedirs(OUTPUT_DIR, exist_ok=True)
#     os.makedirs(TEMP_DIR, exist_ok=True)

#     uid = uuid.uuid4().hex

#     allowed_formats = [
#         "mp3",
#         "wav",
#         "m4a",
#         "opus"
#     ]

#     if format_type not in allowed_formats:
#         format_type = "mp3"


#     output_file = f"{OUTPUT_DIR}/{uid}"
#     temp_file = f"{TEMP_DIR}/{uid}.%(ext)s"


#     ydl_opts = {

#         "format": "bestaudio/best",

#         "outtmpl": temp_file,

#         "postprocessors": [
#             {
#                 "key": "FFmpegExtractAudio",
#                 "preferredcodec": format_type,
#                 "preferredquality": "192",
#             }
#         ],
#     }


#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([link])


#     for file in os.listdir(TEMP_DIR):

#         if file.startswith(uid):

#             old_path = os.path.join(
#                 TEMP_DIR,
#                 file
#             )

#             new_path = f"{output_file}.{format_type}"

#             os.rename(
#                 old_path,
#                 new_path
#             )

#             return new_path


#     raise FileNotFoundError("Audio file not found.")


import os
import uuid
import subprocess
import yt_dlp


OUTPUT_DIR = "static/outputs"
TEMP_DIR = "temp"


# -------------------------------------------------
# Download Audio Source
# -------------------------------------------------

def download_audio_source(url):

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

        "format": "bestaudio/best",

        "outtmpl": output_template,

        "noplaylist": True,

        "quiet": True
    }


    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


    for file in os.listdir(TEMP_DIR):

        if file.startswith(uid):

            return os.path.join(
                TEMP_DIR,
                file
            )


    raise FileNotFoundError(
        "Audio download failed"
    )



# -------------------------------------------------
# Convert Audio Using FFmpeg
# -------------------------------------------------

def convert_audio(
    input_file,
    output_file,
    format_type
):


    formats = {

        "mp3": [
            "-codec:a",
            "libmp3lame",
            "-b:a",
            "192k"
        ],


        "wav": [
            "-codec:a",
            "pcm_s16le"
        ],


        "m4a": [
            "-codec:a",
            "aac",
            "-b:a",
            "192k"
        ],


        "opus": [
            "-codec:a",
            "libopus",
            "-b:a",
            "128k"
        ]

    }


    codec = formats.get(
        format_type,
        formats["mp3"]
    )


    command = [

        "ffmpeg",

        "-y",

        "-i",
        input_file,


        "-vn",

    ] + codec + [

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
            result.stderr
        )


    if not os.path.exists(output_file):

        raise Exception(
            "Audio conversion failed"
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

def extract_audio(
    link: str,
    format_type: str = "mp3"
):


    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )


    allowed = [

        "mp3",
        "wav",
        "m4a",
        "opus"

    ]


    if format_type not in allowed:

        format_type = "mp3"



    uid = uuid.uuid4().hex



    source = None


    output_file = os.path.join(

        OUTPUT_DIR,

        f"{uid}.{format_type}"

    )



    try:


        source = download_audio_source(
            link
        )


        convert_audio(

            source,

            output_file,

            format_type

        )


        return output_file



    finally:


        cleanup(
            source
        )