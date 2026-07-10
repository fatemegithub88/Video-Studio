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
# # Trim Video (Cut)
# # -------------------------------------------------

# def trim_video(start: int, end: int):
#     (
#         ffmpeg
#         .input("video.mp4", ss=start, to=end)
#         .output(
#             "static/outputs/output.mp4",
#             c="copy" 
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

# def create_trimmed_video(url: str, start: int, end: int):

#     download_video(url)

#     trim_video(start, end)

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


#     temp_file = (
#         f"{TEMP_DIR}/{uid}.%(ext)s"
#     )


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
# # Trim Video (Cut)
# # -------------------------------------------------

# def trim_video(
#     input_file,
#     output_file,
#     start: int,
#     end: int
# ):


#     (
#         ffmpeg
#         .input(
#             input_file,
#             ss=start,
#             to=end
#         )
#         .output(
#             output_file,
#             c="copy"
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

# def create_trimmed_video(
#     url: str,
#     start: int,
#     end: int
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
#         f"{OUTPUT_DIR}/{uid}.mp4"
#     )


#     trim_video(
#         video_file,
#         output_file,
#         start,
#         end
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


    ydl_opts = {

        "format": "best[ext=mp4]/best",

        "outtmpl": output_template,

        "merge_output_format": "mp4",

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
        "Video download failed"
    )



# -------------------------------------------------
# Trim Video
# -------------------------------------------------

def trim_video(
    input_file,
    output_file,
    start,
    end
):


    duration = end - start


    if duration <= 0:

        raise ValueError(
            "End time must be greater than start time"
        )



    # First try: Fast cut
    # no re-encode

    command_copy = [

        "ffmpeg",

        "-y",

        "-ss",
        str(start),

        "-i",
        input_file,

        "-t",
        str(duration),


        "-c",
        "copy",


        "-movflags",
        "+faststart",


        output_file

    ]



    result = subprocess.run(

        command_copy,

        stdout=subprocess.DEVNULL,

        stderr=subprocess.PIPE,

        text=True

    )



    if result.returncode == 0 and os.path.exists(output_file):

        return output_file



    # ---------------------------------------------
    # Fallback
    # Re-encode for difficult videos
    # ---------------------------------------------


    if os.path.exists(output_file):

        os.remove(output_file)



    command_encode = [

        "ffmpeg",

        "-y",

        "-ss",
        str(start),

        "-i",
        input_file,

        "-t",
        str(duration),


        "-c:v",
        "libx264",


        "-preset",
        "veryfast",


        "-crf",
        "23",


        "-pix_fmt",
        "yuv420p",


        "-c:a",
        "aac",


        "-b:a",
        "128k",


        "-movflags",
        "+faststart",


        output_file

    ]



    result = subprocess.run(

        command_encode,

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
            "Trim failed"
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

def create_trimmed_video(
    url: str,
    start: int,
    end: int
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


        trim_video(

            video_file,

            output_file,

            start,

            end

        )


        return output_file



    finally:


        cleanup(
            video_file
        )