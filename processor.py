from pathlib import Path

from loguru import logger
from moviepy import VideoFileClip

from config import settings


class VideoProcessor:
    @staticmethod
    def extract_audio(video_path: str | Path) -> Path:
        """
        Extract audio from a video file
        """
        video_path = Path(video_path)
        audio_path = Path(settings.TEMP_DIR) / f"{video_path}.mp3"

        try:
            with VideoFileClip(str(video_path)) as video:
                if video.audio is None:
                    raise ValueError("This video has no audio track")

                logger.info(f"Extracting audio from {video_path}")
                video.audio.write_audiofile(str(audio_path), logger=None)

            logger.success(f"Audio extracted to {audio_path}")
            video.audio.write_audiofile(str(audio_path), logger=None)

            logger.success(f"Audio extracted successfully: {audio_path}")
            return audio_path

        except Exception as e:
            logger.error(f"Failed to extract video: {str(e)}")
            raise e
