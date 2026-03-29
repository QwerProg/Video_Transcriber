from pathlib import Path

from loguru import logger
from moviepy import VideoFileClip


class VideoProcessor:
    @staticmethod
    def extract_audio(video_path: str | Path) -> Path:
        """
        从传入的视频文件中提取音频，保存为 mp3 格式。

        函数会用 MoviePy 调用底层的 FFmpeg 进行音频提取
        如果视频本身没有音频，拦截并报错

        Args:
            video_path (str | Path): 视频文件的路径。

        Returns:
            Path: 提取成功后，生成音频文件的路径。

        Raises:
            ValueError: 如果视频文件没有音频轨道。
            Exception: 底层的 FFmpeg 处理时发生意外抛出。
        """
        video_path = Path(video_path)
        # audio_path = Path(settings.TEMP_DIR) / f"{video_path}.mp3"
        audio_path = video_path.with_suffix(".mp3")

        try:
            logger.info(f"Processing video: {video_path.name}")
            with VideoFileClip(str(video_path)) as video:
                # Check if the video has an audio track
                if video.audio is None:
                    # If there's no audio track, raise an error
                    raise ValueError("This video has no audio track")

                logger.info(f"Extracting audio from {video_path}")

                # `video`: 这是 `MoviePy` 的 `VideoFileClip` 对象，加载在内存中
                # `.audio`: 这是 `VideoFileClip` 的属性，返回一个 `AudioClip` 对象，代表视频的音频轨道。
                # `.write_audiofile()`: 这是 `AudioClip` 的方法，用于将音频写入文件。
                # `str(audio_path)`: 这是音频文件的路径，用于指定写入的目标文件。
                # `logger=None`: 这是一个可选参数，用于指定日志记录器, `bar` 是一个会刷新的进度条。
                video.audio.write_audiofile(str(audio_path), logger="bar")

            logger.success(f"Audio extracted successfully: {audio_path}")
            return audio_path

        except Exception as e:
            logger.error(f"Failed to extract video: {str(e)}")
            raise e
