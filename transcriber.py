import asyncio
from pathlib import Path

from faster_whisper import WhisperModel
from loguru import logger


class AudioTranscriber:
    def __init__(self, model_size: str = "base"):
        logger.info(f"Loading Whisper model: {model_size}... Waitting")

        self.model = WhisperModel(model_size, device="cpu", compute_type="int8")
        logger.success("Whisper model loaded successfully")

    async def transcribe(self, audio_path: Path) -> str:
        """
        Transcribes the audio file at the given path using the loaded Whisper model.

        Args:
            audio_path (Path): Path to the audio file to transcribe.

        Returns:
            str: The transcribed text.
        """
        logger.info(f"Transcribing audio: {audio_path}")

        # Define an internal synchronous function that utilizes CPU computation
        def _do_transcribe():
            segments, _ = self.model.transcribe(str(audio_path), beam_size=5)

            full_text = " "
            for segment in segments:
                full_text += segment.text + " "
            return full_text.strip()

        try:
            text = await asyncio.to_thread(_do_transcribe)
            logger.success(f"Transcription completed: {audio_path}")
            return text
        except Exception as e:
            logger.error(f"Transcription failed: {str(e)}")
            raise e


# Instantiate a singleton transcriber for use throughout the application
transcribe_service = AudioTranscriber()
