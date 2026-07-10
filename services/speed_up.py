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
# # Build Audio Speed Filter
# # -------------------------------------------------

# def build_atempo(speed: float) -> str:
#     """
#     FFmpeg atempo only supports values between 0.5 and 2.0.
#     This function creates a valid filter chain.
#     """

#     filters = []

#     while speed > 2:
#         filters.append("atempo=2")
#         speed /= 2

#     while speed < 0.5:
#         filters.append("atempo=0.5")
#         speed *= 2

#     filters.append(f"atempo={speed:.3f}")

#     return ",".join(filters)


# # -------------------------------------------------
# # Change Speed
# # -------------------------------------------------

# def change_speed(speed: float):

#     video_filter = f"setpts={1/speed}*PTS"

#     audio_filter = build_atempo(speed)

#     (
#         ffmpeg
#         .input("video.mp4")
#         .output(
#             "static/outputs/output.mp4",
#             vf=video_filter,
#             af=audio_filter
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

# def create_speed_video(url: str, speed: float):

#     download_video(url)

#     change_speed(speed)

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
# Build Audio Speed Filter
# -------------------------------------------------

def build_atempo(speed: float) -> str:
    """
    FFmpeg atempo only supports values between 0.5 and 2.0.
    This function creates a valid filter chain.
    """


    filters = []


    while speed > 2:

        filters.append(
            "atempo=2"
        )

        speed /= 2


    while speed < 0.5:

        filters.append(
            "atempo=0.5"
        )

        speed *= 2


    filters.append(
        f"atempo={speed:.3f}"
    )


    return ",".join(filters)



# -------------------------------------------------
# Change Speed
# -------------------------------------------------

def change_speed(
    input_file,
    output_file,
    speed: float
):


    video_filter = (
        f"setpts={1/speed}*PTS"
    )


    audio_filter = build_atempo(
        speed
    )


    (
        ffmpeg
        .input(input_file)
        .output(
            output_file,
            vf=video_filter,
            af=audio_filter
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

def create_speed_video(
    url: str,
    speed: float
):


    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )


    video_file = download_video(url)


    uid = uuid.uuid4().hex


    output_file = (
        f"{OUTPUT_DIR}/{uid}.mp4"
    )


    change_speed(
        video_file,
        output_file,
        speed
    )


    cleanup(video_file)


    return output_file