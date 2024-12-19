from datetime import datetime
from zoneinfo import ZoneInfo

from hackerman_ai.ai.models import News
from hackerman_ai.ai.prompts import PROMPT
from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel


class AIAgent:
    def __init__(self, api_key: str) -> None:
        ai_model = GeminiModel("gemini-1.5-flash", api_key=api_key)
        self.agent = Agent(
            deps_type=str,
            result_type=News,
            model=ai_model,
            system_prompt=PROMPT,
        )

    async def run_prompt(self, news_xml: str) -> News:
        date = datetime.now(ZoneInfo("UTC")).strftime("%Y-%m-%d")  # TODO adjust timezone to sources' tz

        result = await self.agent.run(
            f"Retrieve all news from this date {date}. This is the xml containing the news: {news_xml}"
        )
        return result.data
