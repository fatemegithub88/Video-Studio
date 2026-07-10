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

#     os.makedirs(
#         TEMP_DIR,
#         exist_ok=True
#     )


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


#     raise FileNotFoundError(
#         "Downloaded video not found."
#     )


# # -------------------------------------------------
# # Convert Quality
# # -------------------------------------------------

# def convert_quality(
#     input_file,
#     output_file,
#     quality
# ):


#     quality_map = {

#         "1080p": "1920:1080",

#         "720p": "1280:720",

#         "480p": "854:480",

#         "360p": "640:360",

#         "144p": "256:144"
#     }


#     scale = quality_map.get(
#         quality,
#         "1280:720"
#     )


#     (
#         ffmpeg
#         .input(input_file)
#         .output(
#             output_file,
#             vf=f"scale={scale}"
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

# def create_quality_video(
#     url: str,
#     quality: str
# ):


#     os.makedirs(
#         OUTPUT_DIR,
#         exist_ok=True
#     )


#     video_file = download_video(url)


#     uid = uuid.uuid4().hex

#     output_file = (
#         f"{OUTPUT_DIR}/{uid}.mp4"
#     )


#     convert_quality(
#         video_file,
#         output_file,
#         quality
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

def download_video(url):

    os.makedirs(TEMP_DIR, exist_ok=True)

    uid = uuid.uuid4().hex

    filename = f"{TEMP_DIR}/{uid}.mp4"

    ydl_opts = {
        "format": "bestvideo[height<=1080]+bestaudio/best",
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
# Quality Convert
# -------------------------------------------------

def convert_quality(input_file, output_file, quality):

    heights = {

        "1080p": 1080,
        "720p": 720,
        "480p": 480,
        "360p": 360,
        "240p": 240,
        "144p": 144

    }

    height = heights.get(
        quality,
        720
    )

    command = [

    "ffmpeg",

    "-y",

    "-i",
    input_file,


    "-vf",
    f"scale=-2:{height}",


    "-c:v",
    "libx264",

    "-preset",
    "veryfast",

    "-crf",
    "24",


    "-c:a",
    "aac",

    "-b:a",
    "128k",


    "-pix_fmt",
    "yuv420p",


    "-movflags",
    "+faststart",


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
        raise Exception("Quality conversion failed.")


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

def create_quality_video(url, quality):

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    source = None

    try:

        source = download_video(url)

        uid = uuid.uuid4().hex

        output = f"{OUTPUT_DIR}/{uid}.mp4"

        convert_quality(
            source,
            output,
            quality
        )

        return output

    finally:

        cleanup(source)