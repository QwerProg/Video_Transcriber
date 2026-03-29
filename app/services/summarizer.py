from loguru import logger
from openai import AsyncOpenAI

from app.core.config import settings


class VideoSummarizer:
    def __init__(self):
        if not settings.GOOGLE_API_KEY:
            logger.warning("GEMINI API key not set, summarizer will not work")

        # self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.client = AsyncOpenAI(
            api_key=settings.GOOGLE_API_KEY,
            base_url=settings.GOOGLE_API_BASE,
            timeout=120.0,
            max_retries=2,
        )

    async def summarize(self, text: str) -> str:
        """
        调用 LLM 对长文本进行总结
        """

        if not text or len(text.strip()) < 10:
            return "文本过短，无法总结"

        prompt = f"""
        请以一位专业的视频内容提炼助手，对以下视频转录进行文本总结
        要求：
        1. 提炼核心观点
        2. 语言简练，排版清晰

        原始文本
        {text}
        """

        try:
            logger.info("正在请求 LLM 生成总结...")
            response = await self.client.chat.completions.create(
                model="gemini-3.1-flash-lite-preview",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
            logger.success("LLM 总结生成成功")
            content = response.choices[0].message.content
            if content is None:
                logger.error("LLM 返回的 content 为 None")
                return "总结生成失败：模型未返回文本"
            return content

        except Exception as e:
            logger.error(f"LLM 总结生成失败: {str(e)}")
            return f"生成总结时发生错误: {str(e)}"


summarizer_service = VideoSummarizer()
