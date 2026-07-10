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
        "format": "best[ext=mp4]/best",
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
# Noise Removal
# -------------------------------------------------

def remove_noise(input_file, output_file):

    command = [

        "ffmpeg",

        "-y",

        "-i", input_file,

        # Video
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "23",
        "-pix_fmt", "yuv420p",

        # Audio Noise Removal
        "-af", "afftdn=nr=20:nf=-25",

        "-c:a", "aac",
        "-b:a", "128k",

        "-movflags", "+faststart",

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
        raise Exception("Noise removal failed.")


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

def create_noise_reduced_video(url):

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    source = None

    try:

        source = download_video(url)

        uid = uuid.uuid4().hex

        output = f"{OUTPUT_DIR}/{uid}.mp4"

        remove_noise(
            source,
            output
        )

        return output

    finally:

        cleanup(source)