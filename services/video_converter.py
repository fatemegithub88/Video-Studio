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
import yt_dlp
import ffmpeg


OUTPUT_DIR = "static/outputs"
TEMP_DIR = "temp"



def download_video(url):

    os.makedirs(
        TEMP_DIR,
        exist_ok=True
    )

    uid = uuid.uuid4().hex

    filename = f"{TEMP_DIR}/{uid}.mp4"


    options = {

        "format":
        "best[ext=mp4]/best",

        "outtmpl":
        filename,

        "merge_output_format":
        "mp4",

        "noplaylist":
        True,

        "quiet":
        True
    }


    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])


    if os.path.exists(filename):
        return filename


    for f in os.listdir(TEMP_DIR):

        if f.startswith(uid):
            return os.path.join(
                TEMP_DIR,
                f
            )


    raise Exception(
        "Download failed"
    )



def convert_format(
    input_file,
    output_file,
    output_format
):


    try:


        inp = ffmpeg.input(
            input_file
        )


        video = inp.video

        audio = inp.audio



        if output_format == "webm":

            (
                ffmpeg
                .output(
                    video,
                    audio,
                    output_file,
                    vcodec="libvpx-vp9",
                    acodec="libopus",
                    pix_fmt="yuv420p"
                )
                .global_args(
                    "-loglevel",
                    "error"
                )
                .run(
                    overwrite_output=True
                )
            )


        else:


            (
                ffmpeg
                .output(
                    video,
                    audio,
                    output_file,

                    vcodec="libx264",

                    acodec="aac",

                    video_bitrate="2500k",

                    audio_bitrate="128k",

                    ar=44100,

                    ac=2,

                    pix_fmt="yuv420p",

                    preset="medium",

                    movflags="+faststart"
                )
                .global_args(
                    "-loglevel",
                    "error"
                )
                .run(
                    overwrite_output=True
                )
            )



    except ffmpeg.Error as e:

        print(
            e.stderr.decode(
                errors="ignore"
            )
        )

        raise



    return output_file




def cleanup(path):

    try:

        if path and os.path.exists(path):

            os.remove(path)

    except:

        pass




def create_converted_video(
    url:str,
    output_format:str
):


    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )


    source = None


    try:


        source = download_video(
            url
        )


        uid = uuid.uuid4().hex


        output = (
            f"{OUTPUT_DIR}/{uid}.{output_format}"
        )


        convert_format(
            source,
            output,
            output_format
        )


        return output


    finally:


        cleanup(
            source
        )