import os
import time
import threading
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from services.subtitle import create_subtitled_video
from services.audio_extractor import extract_audio
from services.quality import create_quality_video
from services.compressor import create_compressed_video
from services.audio_boost import create_boosted_video
from services.noise_removal import create_noise_reduced_video
from services.video_trim import create_trimmed_video
from services.video_converter import create_converted_video
from services.speed_up import create_speed_video

# Delete files in outputs/

OUTPUT_DIR = "static/outputs"

def clean_outputs():

    while True:

        time.sleep(30)  
        if not os.path.exists(OUTPUT_DIR):
            continue

        now = time.time()

        for filename in os.listdir(OUTPUT_DIR):

            # Keep git placeholder file
            if filename == ".gitkeep":
                continue

            filepath = os.path.join(OUTPUT_DIR, filename)

            if not os.path.isfile(filepath):
                continue

            if now - os.path.getmtime(filepath) > 30:
                try:
                    os.remove(filepath)
                    print(f"Deleted: {filepath}")
                except Exception as e:
                    print(e)
os.makedirs(
    "static/outputs",
    exist_ok=True
)
app = FastAPI()

threading.Thread(
    target=clean_outputs,
    daemon=True
).start()
app.mount("/outputs", StaticFiles(directory="static/outputs"), name="outputs")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ----------------------------------------
# Request Models
# ----------------------------------------

class VideoRequest(BaseModel):
    url: str


class AudioRequest(BaseModel):
    url: str
    format: str = "mp3"


class QualityRequest(BaseModel):
    url: str
    quality: str


class CompressRequest(BaseModel):
    url: str
    level: str


class AudioBoostRequest(BaseModel):
    url: str
    volume: float = 1.5


class NoiseRequest(BaseModel):
    url: str


class TrimRequest(BaseModel):
    url: str
    start: int
    end: int

class ConvertRequest(BaseModel):
    url: str
    format: str = "mp4"

class SpeedRequest(BaseModel):
    url: str
    speed: float



# ----------------------------------------
# Pages
# ----------------------------------------

@app.get("/")
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@app.get("/api")
def api():
    return {
        "message": "Subtitle AI API",
        "version": "1.0.0",
        "features": [
            "subtitle",
            "audio-extract",
            "quality-change",
            "compress",
            "audio-boost",
            "noise-removal",
            "trim-video"
        ]
    }


# ----------------------------------------
# Subtitle
# ----------------------------------------

@app.post("/subtitle")
def subtitle(data: VideoRequest):

    output_path = create_subtitled_video(data.url)

    return {
        "preview": "/" + output_path.replace("\\", "/")
    }


# ----------------------------------------
# Audio Extractor
# ----------------------------------------

@app.post("/extract-audio")
def audio(data: AudioRequest):

    output_path = extract_audio(
        data.url,
        data.format
    )

    return {
        "preview": "/" + output_path.replace("\\", "/"),
        "type": "audio"
    }


# ----------------------------------------
# Quality Change
# ----------------------------------------

@app.post("/change-quality")
def change_quality(data: QualityRequest):

    output_path = create_quality_video(
        data.url,
        data.quality
    )

    return {
        "preview": "/" + output_path.replace("\\", "/")
    }


# ----------------------------------------
# Compressor
# ----------------------------------------

@app.post("/compress-video")
def compress_video(data: CompressRequest):

    output_path = create_compressed_video(
        data.url,
        data.level
    )

    return {
        "preview": "/" + output_path.replace("\\", "/")
    }


# ----------------------------------------
# Audio Boost
# ----------------------------------------

@app.post("/audio-boost")
def audio_boost(data: AudioBoostRequest):

    output_path = create_boosted_video(
        data.url,
        data.volume
    )

    return {
        "preview": "/" + output_path.replace("\\", "/")
    }


# ----------------------------------------
# Noise Removal
# ----------------------------------------

@app.post("/noise-remove")
def noise_remove(data: NoiseRequest):

    output_path = create_noise_reduced_video(data.url)

    return {
        "preview": "/" + output_path.replace("\\", "/")
    }


# ----------------------------------------
# Trim Video
# ----------------------------------------

@app.post("/trim-video")
def trim_video(data: TrimRequest):

    output_path = create_trimmed_video(
        data.url,
        data.start,
        data.end
    )

    return {
        "preview": "/" + output_path.replace("\\", "/")
    }


# ----------------------------------------
# Video Converter
# ----------------------------------------

@app.post("/convert-video")
def convert(data: ConvertRequest):

    output_path = create_converted_video(
        data.url,
        data.format
    )

    return {
        "preview": "/" + output_path.replace("\\", "/")
    }

# ----------------------------------------
# Speed Up
# ----------------------------------------

@app.post("/change-speed")
def speed(data: SpeedRequest):

    output_path = create_speed_video(
        data.url,
        data.speed
    )

    filename = os.path.basename(output_path)

    return {
        "preview": f"/static/outputs/{filename}"
    }