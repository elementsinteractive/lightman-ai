def get_prompt(news: str) -> str:
    return f"""
            Hi Mr ChatGPT.
            I work for a software consultancty company.
            I will share an xml file containing titles, descriptions and link to cybersecurity news.

            focus only on vulnerabilities that directly affect the technologies that we are using.
            the conditions are:
            I'm only interested on versions of software that have been found to be vulnerable, and that have an associated CVE, and that have been newly discovered.
            I'm only interested in vulnerabilities related only to  Python and Typescript frameworks, web applications, web apps in the cloud and android and ios apps.
            I'm not interested in bad actors or campaigns that exploit vulnerabilities, only in the vulnerabilities themselves.
            don't assume a technology i have not explicitly mentioned.
            I'm not interested in malware, only new CVEs.
            do not invent anything, base your answers on the provided xml.
            Only show results that meet all the criteria.
            This is the xml containing the news: {news}
            """
