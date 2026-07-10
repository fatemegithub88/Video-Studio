# import yt_dlp
# import whisper
# import ffmpeg
# import os
# from deep_translator import GoogleTranslator

# # Load Whisper once
# model = whisper.load_model("tiny")


# # -------------------------------------------------
# # Utils
# # -------------------------------------------------

# def format_timestamp(seconds):
#     hours = int(seconds // 3600)
#     minutes = int((seconds % 3600) // 60)
#     secs = int(seconds % 60)
#     millis = int((seconds % 1) * 1000)
#     return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


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
# # Extract Audio
# # -------------------------------------------------

# def extract_audio(link):
#     ydl_opts = {
#         "format": "bestaudio/best",
#         "outtmpl": "audio_of_video.%(ext)s",
#         "postprocessors": [{
#             "key": "FFmpegExtractAudio",
#             "preferredcodec": "wav",
#         }],
#     }

#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([link])


# # -------------------------------------------------
# # Speech To Text
# # -------------------------------------------------

# def speech_to_text():
#     return model.transcribe("audio_of_video.wav")


# # -------------------------------------------------
# # Translate + Create SRT
# # -------------------------------------------------

# def create_subtitle(result):
#     translator = GoogleTranslator(source="en", target="fa")

#     with open("subtitle_fa.srt", "w", encoding="utf-8") as f:

#         for i, segment in enumerate(result["segments"], start=1):

#             english_text = segment["text"].strip()
#             persian_text = translator.translate(english_text)

#             start = format_timestamp(segment["start"])
#             end = format_timestamp(segment["end"])

#             f.write(f"{i}\n")
#             f.write(f"{start} --> {end}\n")
#             f.write(f"{persian_text}\n\n")

#     with open("subtitle_fa.srt", "a", encoding="utf-8") as f:
#         f.write("\n999\n00:00:01,000 --> 00:00:03,000\nترجمه شده با پایتون\n")


# # -------------------------------------------------
# # Burn Subtitle
# # -------------------------------------------------

# # def burn_subtitle():
# #     input_video = "video.mp4"
# #     input_srt = "subtitle_fa.srt"
# #     output_video = "output.mp4"

# #     ffmpeg.input(input_video).output(
# #         output_video,
# #         vf=f"subtitles={input_srt}"
# #     ).run(overwrite_output=True)
# def burn_subtitle():

#     os.makedirs("static/outputs", exist_ok=True)

#     input_video = "video.mp4"
#     input_srt = "subtitle_fa.srt"
#     output_video = "static/outputs/output.mp4"

#     ffmpeg.input(input_video).output(
#         output_video,
#         vf=f"subtitles={input_srt}"
#     ).run(overwrite_output=True)


# # -------------------------------------------------
# # Cleanup
# # -------------------------------------------------

# def cleanup():
#     os.remove("video.mp4")
#     os.remove("subtitle_fa.srt")
#     os.remove("audio_of_video.wav")


# # -------------------------------------------------
# # Main Pipeline
# # -------------------------------------------------

# def create_subtitled_video(link):
#     download_video(link)

#     extract_audio(link)

#     result = speech_to_text()

#     create_subtitle(result)

#     burn_subtitle()

#     cleanup()

#     return "static/outputs/output.mp4"


# import os
# import uuid
# import yt_dlp
# import whisper
# import ffmpeg
# from deep_translator import GoogleTranslator


# # -------------------------------------------------
# # Directories
# # -------------------------------------------------

# OUTPUT_DIR = "static/outputs"
# TEMP_DIR = "temp"


# # -------------------------------------------------
# # Load Whisper Once
# # -------------------------------------------------

# model = whisper.load_model("tiny")



# # -------------------------------------------------
# # Utils
# # -------------------------------------------------

# def format_timestamp(seconds):

#     hours = int(seconds // 3600)

#     minutes = int((seconds % 3600) // 60)

#     secs = int(seconds % 60)

#     millis = int((seconds % 1) * 1000)


#     return (
#         f"{hours:02d}:"
#         f"{minutes:02d}:"
#         f"{secs:02d},"
#         f"{millis:03d}"
#     )



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
# # Extract Audio
# # -------------------------------------------------

# def extract_audio(link, uid):


#     audio_file = (
#         f"{TEMP_DIR}/{uid}.%(ext)s"
#     )


#     ydl_opts = {

#         "format": "bestaudio/best",

#         "outtmpl": audio_file,

#         "postprocessors": [
#             {
#                 "key": "FFmpegExtractAudio",

#                 "preferredcodec": "wav",
#             }
#         ],
#     }


#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:

#         ydl.download([link])


#     return (
#         f"{TEMP_DIR}/{uid}.wav"
#     )



# # -------------------------------------------------
# # Speech To Text
# # -------------------------------------------------

# def speech_to_text(audio_file):

#     return model.transcribe(
#         audio_file
#     )



# # -------------------------------------------------
# # Translate + Create SRT
# # -------------------------------------------------

# def create_subtitle(
#     result,
#     subtitle_file
# ):

#     translator = GoogleTranslator(
#         source="en",
#         target="fa"
#     )


#     with open(
#         subtitle_file,
#         "w",
#         encoding="utf-8"
#     ) as f:


#         for i, segment in enumerate(
#             result["segments"],
#             start=1
#         ):


#             english_text = (
#                 segment["text"].strip()
#             )


#             persian_text = (
#                 translator.translate(
#                     english_text
#                 )
#             )


#             start = format_timestamp(
#                 segment["start"]
#             )

#             end = format_timestamp(
#                 segment["end"]
#             )


#             f.write(
#                 f"{i}\n"
#             )

#             f.write(
#                 f"{start} --> {end}\n"
#             )

#             f.write(
#                 f"{persian_text}\n\n"
#             )


#         f.write(
#             "\n999\n00:00:01,000 --> 00:00:03,000\nترجمه شده با پایتون\n"
#         )



# # -------------------------------------------------
# # Burn Subtitle
# # -------------------------------------------------

# def burn_subtitle(
#     input_video,
#     input_srt,
#     output_video
# ):


#     (
#         ffmpeg
#         .input(input_video)
#         .output(
#             output_video,
#             vf=f"subtitles={input_srt}"
#         )
#         .run(
#             overwrite_output=True
#         )
#     )



# # -------------------------------------------------
# # Cleanup
# # -------------------------------------------------

# def cleanup(files):

#     for file in files:

#         if os.path.exists(file):

#             os.remove(file)



# # -------------------------------------------------
# # Main Pipeline
# # -------------------------------------------------

# def create_subtitled_video(link):


#     os.makedirs(
#         OUTPUT_DIR,
#         exist_ok=True
#     )


#     uid = uuid.uuid4().hex


#     video_file = download_video(
#         link
#     )


#     audio_file = extract_audio(
#         link,
#         uid
#     )


#     subtitle_file = (
#         f"{TEMP_DIR}/{uid}.srt"
#     )


#     output_file = (
#         f"{OUTPUT_DIR}/{uid}.mp4"
#     )


#     result = speech_to_text(
#         audio_file
#     )


#     create_subtitle(
#         result,
#         subtitle_file
#     )


#     burn_subtitle(
#         video_file,
#         subtitle_file,
#         output_file
#     )


#     cleanup(
#         [
#             video_file,
#             audio_file,
#             subtitle_file
#         ]
#     )


#     return output_file


import os
import uuid
import subprocess
import yt_dlp
import whisper
from deep_translator import GoogleTranslator


OUTPUT_DIR = "static/outputs"
TEMP_DIR = "temp"


# -------------------------------------------------
# Load Whisper Once
# -------------------------------------------------

model = whisper.load_model(
    "tiny",
    device="cpu"
)


# -------------------------------------------------
# Download Video
# -------------------------------------------------

def download_video(url):

    os.makedirs(
        TEMP_DIR,
        exist_ok=True
    )

    uid = uuid.uuid4().hex

    filename = f"{TEMP_DIR}/{uid}.mp4"


    options = {

        "format":
        "bestvideo[height<=720]+bestaudio/best[height<=720]",

        "outtmpl": filename,

        "merge_output_format": "mp4",

        "noplaylist": True,

        "quiet": True
    }


    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])


    if os.path.exists(filename):
        return filename


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
# Extract Audio From Video
# -------------------------------------------------

def extract_audio(video_file, audio_file):

    command = [

        "ffmpeg",

        "-y",

        "-i",
        video_file,

        "-vn",

        "-ac",
        "1",

        "-ar",
        "16000",

        "-codec:a",
        "libmp3lame",

        "-b:a",
        "32k",

        audio_file
    ]


    result = subprocess.run(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True
    )


    if result.returncode != 0:
        raise Exception(result.stderr)


# -------------------------------------------------
# Whisper
# -------------------------------------------------

def speech_to_text(audio_file):

    result = model.transcribe(

        audio_file,

        fp16=False,

        language="en",

        condition_on_previous_text=False,

        temperature=0,

        beam_size=1

    )


    return result


# -------------------------------------------------
# Timestamp
# -------------------------------------------------

def format_timestamp(seconds):

    hours = int(seconds // 3600)

    minutes = int(
        (seconds % 3600) // 60
    )

    secs = int(seconds % 60)

    millis = int(
        (seconds % 1) * 1000
    )


    return (
        f"{hours:02d}:"
        f"{minutes:02d}:"
        f"{secs:02d},"
        f"{millis:03d}"
    )



# -------------------------------------------------
# Create SRT
# -------------------------------------------------

def create_subtitle(result, subtitle_file):


    translator = GoogleTranslator(
        source="en",
        target="fa"
    )


    with open(
        subtitle_file,
        "w",
        encoding="utf-8"
    ) as f:


        for index, segment in enumerate(
            result["segments"],
            start=1
        ):


            text = (
                segment["text"]
                .strip()
            )


            if not text:
                continue


            try:

                translated = translator.translate(
                    text
                )

            except:

                translated = text



            start = format_timestamp(
                segment["start"]
            )


            end = format_timestamp(
                segment["end"]
            )


            f.write(
                f"{index}\n"
            )


            f.write(
                f"{start} --> {end}\n"
            )


            f.write(
                f"{translated}\n\n"
            )



# -------------------------------------------------
# Burn Subtitle
# -------------------------------------------------

def burn_subtitle(
    video_file,
    subtitle_file,
    output_file
):


    command = [

        "ffmpeg",

        "-y",

        "-i",
        video_file,


        "-vf",
        f"subtitles={subtitle_file}",


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

        command,

        stdout=subprocess.PIPE,

        stderr=subprocess.PIPE,

        text=True
    )


    if result.returncode != 0:

        raise Exception(
            result.stderr
        )


    if not os.path.exists(output_file):

        raise Exception(
            "Subtitle burn failed"
        )



# -------------------------------------------------
# Cleanup
# -------------------------------------------------

def cleanup(files):

    for file in files:

        try:

            if file and os.path.exists(file):

                os.remove(file)

        except:

            pass



# -------------------------------------------------
# Main
# -------------------------------------------------

def create_subtitled_video(url):


    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )


    uid = uuid.uuid4().hex


    video_file = None

    audio_file = (
        f"{TEMP_DIR}/{uid}.wav"
    )

    subtitle_file = (
        f"{TEMP_DIR}/{uid}.srt"
    )


    output_file = (
        f"{OUTPUT_DIR}/{uid}.mp4"
    )


    try:


        video_file = download_video(
            url
        )


        extract_audio(
            video_file,
            audio_file
        )


        result = speech_to_text(
            audio_file
        )


        create_subtitle(
            result,
            subtitle_file
        )


        burn_subtitle(
            video_file,
            subtitle_file,
            output_file
        )


        return output_file



    finally:


        cleanup(

            [
                video_file,
                audio_file,
                subtitle_file
            ]

        )