def get_prompt(news: str) -> str:
    return f"""
            Hi Mr ChatGPT.
            I work for a software consultancty company.
            We create web applications, using different Python and Typescript frameworks, deploying to the cloud.
            We also develop ios and android apps.
            I will share an xml file containing titles, descriptions and link to cybersecurity news.

            focus only on vulnerabilities that directly affect the technologies that we are using.
            Show me, in a json format, the links you found to be relevant, how relevant they are, and their title.
            Retrieve all news from today. This is the xml containing the news: {news}
            """
