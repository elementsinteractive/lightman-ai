from hackerman_ai.article.models import ArticlesList

PROMPTS = {
    "eval": """
I'm in software development. I develop web applications and mobile applications.
Given a text with cybersecurity news,
extract all articles showing new vulnerabilities that can affect:
Python, javascript, android and ios development and web and mobile. Also show vulnerabilities about cloud providers.
Do not show malware related news, nor malware campaigns or hackers exploiting vulnerabilities. I'm interested only on newly discovered vulnerabilities or malicious libraries.
very important: Make a distinction between exploits and vulnerabilities being exploited and newly discovered vulnerabilities.
Show also news that can affect software that we use in our day to day work, like browsers, OS vulnerabilities and other things related.
It is very important that I'm only interested on the news that directly relate to our technologies that may impact the development of apps. I don't want any other article that is slightly related. Only those you are sure they are relevant.
Give each of them a relevance score from 1-10 and retrieve all of those with a relevance score >=7."""
}

PROMPTS_CHOICES = list(PROMPTS.keys())


def get_prompt(prompt_name: str) -> str:
    return PROMPTS[prompt_name]


def merge_prompt_with_articles(prompt: str, articles: ArticlesList) -> str:
    return f"""{prompt}
                This is the json:
                {articles}
            """
