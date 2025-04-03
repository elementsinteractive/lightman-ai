def get_prompt(news: str) -> str:
    return (
        """
            Hi Mr ChatGPT.
            I work for a software consultancty company. We create web applications, using different Python and Typescript frameworks, deploying to the cloud.
            We also develop ios and android apps. I will share an xml file containing titles, descriptions and link to cybersecurity news.
            I want also news related to technologies or software that we may use in our day to day work, like operating system-related news, browser news and so on.

            Show me, in a json format, the links you found to be relevant, how relevant they are, and their title.
            """
        f"""
            Retrieve all news from today. This is the xml containing the news: {news}
            """
    )
