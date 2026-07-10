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