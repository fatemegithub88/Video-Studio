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
# # Compress Video
# # -------------------------------------------------

# def compress_video(level):

#     crf_map = {
#         "low": 18,
#         "medium": 28,
#         "high": 35
#     }

#     crf = crf_map[level]

#     ffmpeg.input("video.mp4").output(
#         "static/outputs/output.mp4",
#         vcodec="libx264",
#         crf=crf,
#         preset="medium"
#     ).run(overwrite_output=True)


# # -------------------------------------------------
# # Cleanup
# # -------------------------------------------------

# def cleanup():

#     os.remove("video.mp4")


# # -------------------------------------------------
# # Main Pipeline
# # -------------------------------------------------

# def create_compressed_video(url: str, level: str):

#     download_video(url)

#     compress_video(level)

#     cleanup()

#     return "static/outputs/output.mp4"


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
# # Download Video
# # -------------------------------------------------

# def download_video(link):

#     os.makedirs(TEMP_DIR, exist_ok=True)

#     uid = uuid.uuid4().hex

#     temp_file = f"{TEMP_DIR}/{uid}.%(ext)s"

#     ydl_opts = {

#         "format": "best",

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


#     raise FileNotFoundError("Downloaded video not found.")


# # -------------------------------------------------
# # Compress Video
# # -------------------------------------------------

# def compress_video(input_file, output_file, level):


#     crf_map = {

#         "low": 18,

#         "medium": 28,

#         "high": 35
#     }


#     crf = crf_map.get(
#         level,
#         28
#     )


#     (
#         ffmpeg
#         .input(input_file)
#         .output(
#             output_file,
#             vcodec="libx264",
#             crf=crf,
#             preset="medium"
#         )
#         .run(
#             overwrite_output=True
#         )
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

# def create_compressed_video(url: str, level: str):


#     os.makedirs(
#         OUTPUT_DIR,
#         exist_ok=True
#     )


#     video_file = download_video(url)


#     uid = uuid.uuid4().hex

#     output_file = (
#         f"{OUTPUT_DIR}/{uid}.mp4"
#     )


#     compress_video(
#         video_file,
#         output_file,
#         level
#     )


#     cleanup(video_file)


#     return output_file


import os
import uuid
import shutil
import subprocess
import yt_dlp

OUTPUT_DIR = "static/outputs"
TEMP_DIR = "temp"


# -------------------------------------------------
# Download Video
# -------------------------------------------------

def download_video(url):

    os.makedirs(TEMP_DIR, exist_ok=True)

    uid = uuid.uuid4().hex

    filename = f"{TEMP_DIR}/{uid}.mp4"

    ydl_opts = {
        "format": "best[ext=mp4]/best",
        "merge_output_format": "mp4",
        "outtmpl": filename,
        "quiet": True,
        "noplaylist": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    if os.path.exists(filename):
        return filename

    for file in os.listdir(TEMP_DIR):
        if file.startswith(uid):
            return os.path.join(TEMP_DIR, file)

    raise FileNotFoundError("Video download failed.")


# -------------------------------------------------
# Compress
# -------------------------------------------------

def compress_video(input_file, output_file, level):

    crf_values = {
        "low": 18,
        "medium": 28,
        "high": 35
    }

    crf = crf_values.get(level, 28)

    command = [
        "ffmpeg",
        "-y",

        "-i", input_file,

        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", str(crf),

        "-c:a", "aac",
        "-b:a", "128k",

        "-movflags", "+faststart",

        "-pix_fmt", "yuv420p",

        output_file
    ]

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        raise Exception(result.stderr)

    if not os.path.exists(output_file):
        raise Exception("Compression failed.")


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
# Main
# -------------------------------------------------

def create_compressed_video(url, level):

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    source = None

    try:

        source = download_video(url)

        uid = uuid.uuid4().hex

        output = f"{OUTPUT_DIR}/{uid}.mp4"

        compress_video(
            source,
            output,
            level
        )

        return output

    finally:

        cleanup(source)