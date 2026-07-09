# 🎬 Video Studio

A web-based video processing toolkit featuring subtitle generation, media conversion, audio extraction, and video enhancement, powered by **FastAPI**, **FFmpeg**, **Whisper**, and **yt-dlp**.

The application allows users to process online videos directly from a URL, preview the result instantly using Plyr, and download the processed output.

---

## ✨ Features

- 🎬 AI Subtitle Generation (English ➜ Persian)
- 🎧 Extract Audio
- 📺 Change Video Quality
- 🗜 Video Compression
- 🔊 Audio Boost
- 🔊 Noise Removal
- ✂ Trim Video
- 🔄 Convert Video Format
- ⚡ Change Playback Speed
- ▶ Online Preview with Plyr
- ⬇ Direct Download
- 🧹 Automatic Output Cleanup

---

## 🛠 Tech Stack

### Backend

- FastAPI
- Python
- Whisper AI
- FFmpeg
- yt-dlp

### Frontend

- HTML5
- CSS3
- Vanilla JavaScript
- Plyr

---


## 🚀 Installation

Clone the repository

```bash
git clone https://github.com/yourusername/AI-Video-Studio.git
```

Go to project

```bash
cd AI-Video-Studio
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run

```bash
uvicorn main:app --reload
```

Open

```
http://127.0.0.1:8000
```

---

## 🌐 API Endpoints

| Endpoint | Description |
|----------|-------------|
| POST /subtitle | Generate subtitles |
| POST /extract-audio | Extract audio |
| POST /change-quality | Change resolution |
| POST /compress-video | Compress video |
| POST /audio-boost | Increase volume |
| POST /noise-remove | Remove background noise |
| POST /trim-video | Trim video |
| POST /convert-video | Convert format |
| POST /change-speed | Change playback speed |

---