from typing import Never

from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel


class AIAgent:
    def __init__(self, api_key: str) -> None:
        ai_model = GeminiModel("gemini-1.5-flash", api_key=api_key)
        self.agent: Agent[Never, Never] = Agent(
            model=ai_model,
        )

    async def run_prompt(self, prompt: str) -> str:
        result = await self.agent.run(prompt)
        return result.data
