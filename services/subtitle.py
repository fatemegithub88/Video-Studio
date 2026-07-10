import os
import uuid
import subprocess
import gc

import yt_dlp
import whisper

from deep_translator import GoogleTranslator



OUTPUT_DIR = "static/outputs"
TEMP_DIR = "temp"



os.makedirs(
    TEMP_DIR,
    exist_ok=True
)



# -----------------------------
# Whisper Load
# -----------------------------

model = whisper.load_model(
    "tiny",
    device="cpu"
)



# -----------------------------
# Download Video
# -----------------------------

def download_video(url):


    uid = uuid.uuid4().hex


    filename = os.path.join(
        TEMP_DIR,
        f"{uid}.mp4"
    )


    options = {

        "format":
        "bestvideo[height<=720]+bestaudio/best",

        "outtmpl":
        filename,

        "merge_output_format":
        "mp4",

        "noplaylist":
        True,

        "quiet":
        True,

        "no_warnings":
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




# -----------------------------
# Extract Audio
# -----------------------------

def extract_audio(
    video,
    audio
):


    command = [

        "ffmpeg",

        "-y",

        "-i",
        video,

        "-vn",

        "-ac",
        "1",

        "-ar",
        "16000",

        "-codec:a",
        "libmp3lame",

        "-b:a",
        "32k",

        audio
    ]



    result = subprocess.run(

        command,

        stdout=subprocess.DEVNULL,

        stderr=subprocess.PIPE,

        text=True

    )



    if result.returncode != 0:

        raise Exception(
            result.stderr
        )




# -----------------------------
# Whisper
# -----------------------------

def speech_to_text(audio):


    with open(audio,"rb"):

        result = model.transcribe(

            audio,

            fp16=False,

            language="en",

            temperature=0,

            beam_size=1,

            best_of=1,

            condition_on_previous_text=False,

            verbose=False

        )



    gc.collect()


    return result





# -----------------------------
# Timestamp
# -----------------------------

def format_timestamp(seconds):


    h = int(seconds // 3600)

    m = int(
        (seconds % 3600)//60
    )

    s = int(seconds % 60)

    ms = int(
        (seconds % 1)*1000
    )


    return (
        f"{h:02}:{m:02}:{s:02},{ms:03}"
    )




# -----------------------------
# Create Subtitle
# -----------------------------

def create_subtitle(
    result,
    file
):


    translator = GoogleTranslator(

        source="en",

        target="fa"

    )



    with open(

        file,

        "w",

        encoding="utf-8"

    ) as f:



        index = 1



        for segment in result["segments"]:


            text = segment["text"].strip()



            if not text:

                continue



            try:

                translated = translator.translate(
                    text
                )


            except Exception:

                translated = text




            f.write(

                f"{index}\n"

            )


            f.write(

                f"{format_timestamp(segment['start'])} --> {format_timestamp(segment['end'])}\n"

            )


            f.write(

                translated+"\n\n"

            )


            index += 1



# -----------------------------
# Burn Subtitle
# -----------------------------

def burn_subtitle(

    video,

    subtitle,

    output

):


    command = [

        "ffmpeg",

        "-y",

        "-threads",
        "2",

        "-i",

        video,


        "-vf",

        f"subtitles={subtitle}",


        "-c:v",

        "libx264",


        "-preset",

        "veryfast",


        "-crf",

        "26",


        "-pix_fmt",

        "yuv420p",


        "-c:a",

        "aac",


        "-b:a",

        "96k",


        "-movflags",

        "+faststart",


        output

    ]



    result = subprocess.run(

        command,

        stdout=subprocess.DEVNULL,

        stderr=subprocess.PIPE,

        text=True

    )



    if result.returncode != 0:

        raise Exception(
            result.stderr
        )





# -----------------------------
# Cleanup
# -----------------------------

def cleanup(files):


    for f in files:

        try:

            if f and os.path.exists(f):

                os.remove(f)


        except:

            pass




# -----------------------------
# Main
# -----------------------------

def create_subtitled_video(url):


    uid = uuid.uuid4().hex



    video_file = None


    audio_file = (
        f"{TEMP_DIR}/{uid}.mp3"
    )


    subtitle_file = (
        f"{TEMP_DIR}/{uid}.srt"
    )


    output_file = (

        f"{OUTPUT_DIR}/{uid}.mp4"

    )



    try:


        os.makedirs(
            OUTPUT_DIR,
            exist_ok=True
        )



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


        del result

        gc.collect()



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