from hackerman_ai.article.models import ArticlesList

PROMPTS = {
    "eval": """
I'm in software development. I develop web applications and mobile applications.
Given a text with cybersecurity news,
Give a score 1-10 to each one of all the articles, depending on how relevant they are to me. Give me back the articles with the relevance that you think they have.'
The criteria to follow is:
- I work with Python, javascript, android and ios development and web and mobile. Also show vulnerabilities about cloud providers that are directly related with development.
- I'm only interested in libraries vulnerabilities when they directly impact the work of a web or mobile developer
- Even if it's a web development vulnerability but does not belong to the techonolgies that I'm interested in, it is not relevant for me.
- I'm not interested in malware related news, nor malware campaigns or hackers exploiting vulnerabilities or rootkits using already known vulnerabilities. I'm interested only in newly discovered vulnerabilities.
- very important: Make a distinction between exploits and vulnerabilities being exploited and newly discovered vulnerabilities.
- It is very important that those articles not related to the technologies I use are not relevant for me.
""",
}

PROMPTS_CHOICES = list(PROMPTS.keys())


def get_prompt(prompt_name: str) -> str:
    return PROMPTS[prompt_name]


def merge_prompt_with_articles(prompt: str, articles: ArticlesList) -> str:
    return f"""{prompt}
                This is the json:
                {articles}
            """
