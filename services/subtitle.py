import yt_dlp
import whisper
import ffmpeg
import os
from deep_translator import GoogleTranslator

# Load Whisper once
model = whisper.load_model("tiny")


# -------------------------------------------------
# Utils
# -------------------------------------------------

def format_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


# -------------------------------------------------
# Download Video
# -------------------------------------------------

def download_video(link):
    ydl_opts = {
        "format": "best",
        "outtmpl": "video.%(ext)s"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])


# -------------------------------------------------
# Extract Audio
# -------------------------------------------------

def extract_audio(link):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "audio_of_video.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])


# -------------------------------------------------
# Speech To Text
# -------------------------------------------------

def speech_to_text():
    return model.transcribe("audio_of_video.wav")


# -------------------------------------------------
# Translate + Create SRT
# -------------------------------------------------

def create_subtitle(result):
    translator = GoogleTranslator(source="en", target="fa")

    with open("subtitle_fa.srt", "w", encoding="utf-8") as f:

        for i, segment in enumerate(result["segments"], start=1):

            english_text = segment["text"].strip()
            persian_text = translator.translate(english_text)

            start = format_timestamp(segment["start"])
            end = format_timestamp(segment["end"])

            f.write(f"{i}\n")
            f.write(f"{start} --> {end}\n")
            f.write(f"{persian_text}\n\n")

    with open("subtitle_fa.srt", "a", encoding="utf-8") as f:
        f.write("\n999\n00:00:01,000 --> 00:00:03,000\nترجمه شده با پایتون\n")


# -------------------------------------------------
# Burn Subtitle
# -------------------------------------------------

# def burn_subtitle():
#     input_video = "video.mp4"
#     input_srt = "subtitle_fa.srt"
#     output_video = "output.mp4"

#     ffmpeg.input(input_video).output(
#         output_video,
#         vf=f"subtitles={input_srt}"
#     ).run(overwrite_output=True)
def burn_subtitle():

    os.makedirs("static/outputs", exist_ok=True)

    input_video = "video.mp4"
    input_srt = "subtitle_fa.srt"
    output_video = "static/outputs/output.mp4"

    ffmpeg.input(input_video).output(
        output_video,
        vf=f"subtitles={input_srt}"
    ).run(overwrite_output=True)


# -------------------------------------------------
# Cleanup
# -------------------------------------------------

def cleanup():
    os.remove("video.mp4")
    os.remove("subtitle_fa.srt")
    os.remove("audio_of_video.wav")


# -------------------------------------------------
# Main Pipeline
# -------------------------------------------------

def create_subtitled_video(link):
    download_video(link)

    extract_audio(link)

    result = speech_to_text()

    create_subtitle(result)

    burn_subtitle()

    cleanup()

    return "static/outputs/output.mp4"