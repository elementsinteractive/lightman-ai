from enum import StrEnum

from hackerman_ai.article.models import ArticlesList


class Prompts(StrEnum):
    SHORT_PROMPT = """
                    I'm in software development. Given text with cybersecurity news,
                    extract only new CVEs and vulnerabilities that:
                    Affect Python/TypeScript frameworks, web/cloud apps, Android/iOS
                    Have known vulnerable versions
                    Exclude malware, actors, campaigns
                    Use only listed tech, make no assumptions
                    Must meet all criteria, use only text content
                  """


def add_articles_to_prompt(prompt: Prompts, articles: ArticlesList) -> str:
    return f"""{prompt}
                This is the json:
                {articles}
            """
