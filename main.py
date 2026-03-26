import os
import shutil
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from loguru import logger

from config import settings
from processor import VideoProcessor


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up Video Transcriber backend")

    if not os.path.exists(settings.TEMP_DIR):
        os.makedirs(settings.TEMP_DIR)
        logger.info(f"Created Temp Dir: {settings.TEMP_DIR}")
    else:
        logger.info(f"Temp Dir is exists: {settings.TEMP_DIR}")

    yield

    logger.warning("Shutting down Video Transcriber backend")


# Initialize FastAPI app
app = FastAPI(
    title="Video Transcriber",
    description="A FastAPI backend for transcribing videos.",
    lifespan=lifespan,
)


# A Testing
@app.get("/health")
async def health_check():
    logger.info("Health check called")
    return {"status": "ok", "message": "FastAPI is running"}


@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    content_type = file.content_type or ""
    if not content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="Only video files are allowed.")

    filename = file.filename or "uploaded_video.mp4"
    video_path = Path(settings.TEMP_DIR) / filename

    try:
        logger.info(f"Uploaded file: {file.filename}")

        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        audio_path = VideoProcessor.extract_audio(video_path)

        return {
            "message": "Video uploaded successfully",
            "video_path": str(video_path),
            "audio_path": str(audio_path),
        }

    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
