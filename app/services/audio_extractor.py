# import yt_dlp

# # ---------------------------------
# # Extract Audio (with format support)
# # ---------------------------------

# def extract_audio(link: str, format_type: str = "mp3"):

#     allowed_formats = ["mp3", "wav", "m4a", "opus"]

#     if format_type not in allowed_formats:
#         format_type = "mp3"

#     ydl_opts = {
#         "format": "bestaudio/best",
#         "outtmpl": "audio_of_video.%(ext)s",
#         "postprocessors": [{
#             "key": "FFmpegExtractAudio",
#             "preferredcodec": format_type,
#             "preferredquality": "192",
#         }],
#     }

#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([link])

#     return f"audio_of_video.{format_type}"


import os
import yt_dlp

OUTPUT_DIR = "static/outputs"

# ---------------------------------
# Extract Audio (with format support)
# ---------------------------------

def extract_audio(link: str, format_type: str = "mp3"):

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    allowed_formats = ["mp3", "wav", "m4a", "opus"]

    if format_type not in allowed_formats:
        format_type = "mp3"

    output_name = os.path.join(OUTPUT_DIR, "audio")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_name + ".%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": format_type,
            "preferredquality": "192",
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])

    return f"{output_name}.{format_type}"