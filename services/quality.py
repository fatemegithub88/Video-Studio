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


    output_template = os.path.join(
        TEMP_DIR,
        f"{uid}.%(ext)s"
    )


    ydl_opts = {

        "format": "bestvideo+bestaudio/best",

        "outtmpl": output_template,

        "merge_output_format": "mp4"

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
# Convert Quality
# -------------------------------------------------

def convert_quality(
        input_file,
        output_file,
        quality
):


    quality_map = {

        "1080p": 1080,

        "720p": 720,

        "480p": 480,

        "360p": 360,

        "144p": 144

    }


    height = quality_map.get(
        quality,
        720
    )


    try:

        (
            ffmpeg
            .input(input_file)
            .output(

                output_file,

                vf=f"scale=-2:{height}",

                vcodec="libx264",

                acodec="aac",

                audio_bitrate="128k",

                pix_fmt="yuv420p",

                preset="medium",

                movflags="faststart"

            )
            .run(

                overwrite_output=True,

                capture_stdout=True,

                capture_stderr=True

            )
        )


    except ffmpeg.Error as e:

        print(
            "FFMPEG ERROR:"
        )

        print(
            e.stderr.decode()
        )

        raise



# -------------------------------------------------
# Cleanup
# -------------------------------------------------

def cleanup(file_path):

    if os.path.exists(file_path):

        os.remove(file_path)



# -------------------------------------------------
# Main Pipeline
# -------------------------------------------------

def create_quality_video(
        url: str,
        quality: str
):


    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )


    video_file = download_video(url)


    uid = uuid.uuid4().hex


    output_file = os.path.join(
        OUTPUT_DIR,
        f"{uid}.mp4"
    )


    convert_quality(

        video_file,

        output_file,

        quality

    )


    cleanup(video_file)


    return output_file