# import yt_dlp
# import ffmpeg
# import os

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
#     output_format: mp4 | mkv | webm | mov
#     """

#     (
#         ffmpeg.input("video.mp4").output(
#     f"output.{output_format}",
#     vcodec="libx264",
#     acodec="aac"
# ).run(overwrite_output=True)
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

# def create_converted_video(url: str, output_format: str):

#     download_video(url)

#     convert_format(output_format)

#     cleanup()

#     return f"static/outputs/output.{output_format}"





import yt_dlp
import ffmpeg
import os

OUTPUT_DIR = "static/outputs"

# -------------------------------------------------
# Download Video (any format)
# -------------------------------------------------

def download_video(link):

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "outtmpl": "video.%(ext)s"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])


# -------------------------------------------------
# Convert Format
# -------------------------------------------------

def convert_format(output_format: str):

    """
    output_format:
    mp4 | mkv | webm | mov
    """

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    output_file = os.path.join(
        OUTPUT_DIR,
        f"output.{output_format}"
    )

    (
        ffmpeg
        .input("video.mp4")
        .output(
            output_file,
            vcodec="libx264",
            acodec="aac"
        )
        .run(overwrite_output=True)
    )

    return output_file


# -------------------------------------------------
# Cleanup
# -------------------------------------------------

def cleanup():

    if os.path.exists("video.mp4"):
        os.remove("video.mp4")


# -------------------------------------------------
# Main Pipeline
# -------------------------------------------------

def create_converted_video(url: str, output_format: str):

    download_video(url)

    output_path = convert_format(output_format)

    cleanup()

    return output_path