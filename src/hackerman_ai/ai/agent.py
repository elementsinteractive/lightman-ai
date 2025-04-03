from typing import Never

from hackerman_ai.ai.models import News
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel


class AIAgent:
    def __init__(self) -> None:
        ai_model = OpenAIModel("gpt-4o")
        self.agent: Agent[Never, News] = Agent(model=ai_model, result_type=News)

    async def run_prompt(self, prompt: str) -> News:
        result = await self.agent.run(prompt)
        return result.data
