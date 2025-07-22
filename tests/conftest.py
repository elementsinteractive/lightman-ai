import os
from collections.abc import Generator, Iterator
from contextlib import contextmanager
from typing import Any
from unittest.mock import AsyncMock, Mock, patch

import pytest
import stamina
from lightman_ai.article.models import ArticlesList, SelectedArticle
from lightman_ai.integrations.service_desk.integration import ServiceDeskIntegration
from lightman_ai.sources.the_hacker_news import TheHackerNewsSource
from stamina._core import _RetryContextIterator


def pytest_configure() -> None:
    os.environ["OPENAI_API_KEY"] = "dummy"
    os.environ["GOOGLE_API_KEY"] = "dummy"


@pytest.fixture
def patch_service_desk_retry_wait_max() -> Generator[None, Any, None]:
    original_retry_context = stamina.retry_context

    def patched_retry_context(*args: Any, **kwargs: Any) -> _RetryContextIterator:
        kwargs["wait_max"] = 0
        return original_retry_context(*args, **kwargs)

    with patch("stamina.retry_context", new=patched_retry_context) as mock:
        yield mock


@pytest.fixture
def selected_articles() -> list[SelectedArticle]:
    """Create test articles for service desk issue creation."""
    return [
        SelectedArticle(
            title="Critical Security Vulnerability in Popular Library",
            link="https://example.com/article1",
            why_is_relevant="This affects our production systems",
            relevance_score=9,
        ),
        SelectedArticle(
            title="New Attack Vector Discovered",
            link="https://example.com/article2",
            why_is_relevant="Could impact our infrastructure",
            relevance_score=8,
        ),
    ]


@pytest.fixture
def mock_service_desk() -> Mock:
    """Create a mock ServiceDeskIntegration."""
    mock = Mock(spec=ServiceDeskIntegration)
    mock.create_request_of_type = AsyncMock(return_value="PROJ-123")
    return mock


@pytest.fixture
def thn_xml() -> str:
    return """<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><rss xmlns:atom=\"http://www.w3.org/2005/Atom\"
        xmlns:content=\"http://purl.org/rss/1.0/modules/content/\" xmlns:dc=\"http://purl.org/dc/group/1.1/\"
        xmlns:itunes=\"http://www.itunes.com/dtds/podcast-1.0.dtd\" xmlns:media=\"http://search.yahoo.com/mrss/\"
        xmlns:slash=\"http://purl.org/rss/1.0/modules/slash/\" xmlns:sy=\"http://purl.org/rss/1.0/modules/syndication/\"
        xmlns:wfw=\"http://wellformedweb.org/CommentAPI/\" version=\"2.0\"><channel><title>The
        Hacker News</title><link>https://thehackernews.com</link><description>Most
        trusted, widely-read independent cybersecurity news source for everyone; supported
        by hackers and IT professionals \u2014 Send TIPs to admin@thehackernews.com</description><language>en-us</language><lastBuildDate>Fri,
        04 Apr 2025 17:32:59 +0530</lastBuildDate><sy:updatePeriod>hourly</sy:updatePeriod><sy:updateFrequency>1</sy:updateFrequency><atom:link
        href=\"https://feeds.feedburner.com/TheHackersNews\" rel=\"self\" type=\"application/rss+xml\"/><item><title>SpotBugs
        Access Token Theft Identified as Root Cause of GitHub Supply Chain Attack</title><description><![CDATA[The
        cascading supply chain attack that initially targeted Coinbase before becoming
        more widespread to single out users of the \"tj-actions/changed-files\" GitHub
        Action has been traced further back to the theft of a personal access token
        (PAT) related to SpotBugs.\n\"The attackers obtained initial access by taking
        advantage of the GitHub Actions workflow of SpotBugs, a popular open-source
        tool for]]></description><link>https://thehackernews.com/2025/04/spotbugs-access-token-theft-identified.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/04/spotbugs-access-token-theft-identified.html</guid><pubDate>Fri,
        04 Apr 2025 17:58:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjCJMdiwIavBa0wI3kGPkWYZD-72a5YNecTRZCai6gVL3dtWmeAKH9BdSk3-xf2w_IPDZysjnE0WNCqZuNdzNoGvmfri07SXOlF19YZ2QqboQ0dglgzBAcZLK29Urky4PSeKc0fQd3J2YatwcuwQE-ASUMCidjt98twk5i7ebhWV2d-qHAsGQn5vYgVwKf4/s1600/github-hack.jpg\"/></item><item><title>Have
        We Reached a Distroless Tipping Point?</title><description><![CDATA[There\u2019s
        a virtuous cycle in technology that pushes the boundaries of what\u2019s being
        built and how it\u2019s being used. A new technology development emerges and
        captures the world's attention. People start experimenting and discover novel
        applications, use cases, and approaches to maximize the innovation's potential.
        These use cases generate significant value, fueling demand for the next iteration
        of]]></description><link>https://thehackernews.com/2025/04/have-we-reached-distroless-tipping-point.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/04/have-we-reached-distroless-tipping-point.html</guid><pubDate>Fri,
        04 Apr 2025 16:27:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhrDCWS6B07Vztre5CTnGdL-I37Lu0C34z3XQa5fb1S9C-V_JZNoMReZ2tMCvArfIpt6oTEe_fodu880Z3kchFv4xa6G75J5Gqc413hlGjzLnEC2TtQmGVn5A76S6dzcRXvkwq3OzE9GhO2QuUGssSP1pg1m-x3EzIBUiCLyUgqa1qPMbYgqCS7oUHJHO4/s1600/chaingaurddev.jpg\"/></item><item><title>Critical
        Ivanti Flaw Actively Exploited to Deploy TRAILBLAZE and BRUSHFIRE Malware</title><description><![CDATA[Ivanti
        has disclosed details of a now-patched critical security vulnerability impacting
        its Connect Secure that has come under active exploitation in the wild.\nThe
        vulnerability, tracked as CVE-2025-22457 (CVSS score: 9.0), concerns a case
        of a stack-based buffer overflow that could be exploited to execute arbitrary
        code on affected systems.\n\"A stack-based buffer overflow in Ivanti Connect]]></description><link>https://thehackernews.com/2025/04/critical-ivanti-flaw-actively-exploited.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/04/critical-ivanti-flaw-actively-exploited.html</guid><pubDate>Fri,
        04 Apr 2025 11:37:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjCltg902mTaOYxU2hZDJqQJhi9eJluvxfnbIAsb0TGxGbkPpcC2bFLnQmwCw0xC-ve4pgNLlSGzT1rUVmaIyWGodNQihyphenhyphenWcgsL9fUGrMAcfYJ-zz2XtKlN-7-L6WZF6Md48cG9sQYj_xsdC55um9N2jlmq-wKw5C3FeBC-IsEhCmuihjjNxXsFakuZOeyB/s1600/hackers.jpg\"/></item><item><title>OPSEC
        Failure Exposes Coquettte\u2019s Malware Campaigns on Bulletproof Hosting
        Servers</title><description><![CDATA[A novice cybercrime actor has been observed
        leveraging the services of a Russian bulletproof hosting (BPH) provider called
        Proton66 to facilitate their operations.\nThe findings come from DomainTools,
        which detected the activity after it discovered a phony website named cybersecureprotect[.]com
        hosted on Proton66 that masqueraded as an antivirus service.\nThe threat intelligence
        firm said it]]></description><link>https://thehackernews.com/2025/04/opsec-failure-exposes-coquetttes.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/04/opsec-failure-exposes-coquetttes.html</guid><pubDate>Fri,
        04 Apr 2025 11:36:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEinjtUMF19M1JEXdaLMbMDAmPNKflZgbYuwqdLc8ll6_lmTivextTVfdGVPHVEn_6eAovS_QCjua0l6HDL-tgs2Pzy9wpfVOkxF_a_4FwAyBAZEXha-7rpgQpNalwH3LpO0IdRMh4YAeD-rzXyXaaqx_kn2NttO2sJ35SDXk9OTBQ35pfpOVNSBKvDJS2K2/s1600/hacker-exposed.jpg\"/></item><item><title>CERT-UA
        Reports Cyberattacks Targeting Ukrainian State Systems with WRECKSTEEL Malware</title><description><![CDATA[The
        Computer Emergency Response Team of Ukraine (CERT-UA) has revealed that no
        less than three cyber attacks were recorded against state administration bodies
        and critical infrastructure facilities in the country with an aim to steal
        sensitive data.\nThe campaign, the agency said, involved the use of compromised
        email accounts to send phishing messages containing links pointing to legitimate]]></description><link>https://thehackernews.com/2025/04/cert-ua-reports-cyberattacks-targeting.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/04/cert-ua-reports-cyberattacks-targeting.html</guid><pubDate>Fri,
        04 Apr 2025 10:24:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiMxvAwVD_wGKDTL5DasfV5uoYt8gqjhd6jismbKI0mAkH46-2RttjCnagGH4bUpmGOZe6Ijc6whb9u0iNcJh1yxsFFpVw75Tfj7fosyTmYnxyOV_EZy0Dy-7CIlzICWyLFwejIDhLIPYou7EM8BslM5H1bnQD1Btg_hTddOpgApGQDCrzawYTgTU1uNokp/s1600/cyberattacks.jpg\"/></item><item><title>Critical
        Flaw in Apache Parquet Allows Remote Attackers to Execute Arbitrary Code</title><description><![CDATA[A
        maximum severity security vulnerability has been disclosed in Apache Parquet's
        Java Library that, if successfully exploited, could allow a remote attacker
        to execute arbitrary code on susceptible instances.\nApache Parquet is a free
        and open-source columnar data file format that's designed for efficient data
        processing and retrieval, providing support for complex data, high-performance]]></description><link>https://thehackernews.com/2025/04/critical-flaw-in-apache-parquet-allows.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/04/critical-flaw-in-apache-parquet-allows.html</guid><pubDate>Fri,
        04 Apr 2025 09:08:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEg8SZm2bMnr5sNUMNrpVcl2Z6VCjSWYXv-MzAMnuywVJnQzC0XE_kAA7iyOHbhHif8FrVBbx3lYCnwzec0agkDYE66k-FVRJOECGH7ohydohuo55kepS81NIk63PLR7ZcShnHRTAb4dvGSsNMUyi_PVRrwgcpXVUw5bbc9t0bjggrtf0zQW8umDl_iHJGUE/s1600/apache.jpg\"/></item><item><title>Microsoft
        Warns of Tax-Themed Email Attacks Using PDFs and QR Codes to Deliver Malware</title><description><![CDATA[Microsoft
        is warning of several phishing campaigns that are leveraging tax-related themes
        to deploy malware and steal credentials.\n\"These campaigns notably use redirection
        methods such as URL shorteners and QR codes contained in malicious attachments
        and abuse legitimate services like file-hosting services and business profile
        pages to avoid detection,\" Microsoft said in a report shared with The]]></description><link>https://thehackernews.com/2025/04/microsoft-warns-of-tax-themed-email.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/04/microsoft-warns-of-tax-themed-email.html</guid><pubDate>Thu,
        03 Apr 2025 23:09:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEh5Xcc9Zn_nbhrMNv2piZYznJXBb7bqlU0YWcAidDMQz8iQkNOYKozLC2PD0NDqBWWJoyK1ySs2rDCXnUPh4JJN0EKtWtBr7iGL4C5QOeyLDn8GTp3LoaAQRCIEyQK73PrsP8ACVH7kAEJJFcrQx_iNQRmTnYbsmAcQmEUTL29qjDeNljuzlEOoFFM3ywiG/s1600/phish.jpg\"/></item><item><title>Lazarus
        Group Targets Job Seekers With ClickFix Tactic to Deploy GolangGhost Malware</title><description><![CDATA[The
        North Korean threat actors behind Contagious Interview have adopted the increasingly
        popular ClickFix social engineering tactic to lure job seekers in the cryptocurrency
        sector to deliver a previously undocumented Go-based backdoor called GolangGhost
        on Windows and macOS systems.\nThe new activity, assessed to be a continuation
        of the campaign, has been codenamed ClickFake Interview by]]></description><link>https://thehackernews.com/2025/04/lazarus-group-targets-job-seekers-with.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/04/lazarus-group-targets-job-seekers-with.html</guid><pubDate>Thu,
        03 Apr 2025 17:52:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhO_c-XOYl7-Hq892uDpCyqNOVKadcDQO2mWTDDiFRoFdtPMOIMfDbWkh6t6LkdQkvpJEId71tppdArll4nPbPV59fKOszhtlr2_c1yeKz-Ri5-ugi0uD3XD4NyD_43flOfyk1d8WaiY8R48Pgpat6V-JvwKebnK75zGRjUq_fRWHgOZzK3DZoatWKjOlKa/s1600/ClickFix-malware.jpg\"/></item><item><title>AI
        Threats Are Evolving Fast \u2014 Learn Practical Defense Tactics in this Expert
        Webinar</title><description><![CDATA[The rules have changed. Again. Artificial
        intelligence is bringing powerful new tools to businesses. But it's also giving
        cybercriminals smarter ways to attack. They\u2019re moving quicker, targeting
        more precisely, and slipping past old defenses without being noticed.\nAnd
        here's the harsh truth: If your security strategy hasn\u2019t evolved with
        AI in mind, you\u2019re already behind.\nBut you\u2019re not alone\u2014and]]></description><link>https://thehackernews.com/2025/04/ai-threats-are-evolving-fast-learn.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/04/ai-threats-are-evolving-fast-learn.html</guid><pubDate>Thu,
        03 Apr 2025 16:55:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjTSVTRKCYISiJJmvIuWiQKnfQ4IaR8H9jM4tXaJzvtZDSrna4Vb-zPpHwZR7A_DnXzibnEsuLVGnvt_zZKEityIGQoliSJiMlKodysLyoTF4Tujx2aXsiCae7gUX415hYdRIbl-32PelGkJN8QWBHyFyBCuX5Ur98BQ9eEmFkPW8M6d17IRDrU9Egrwevr/s1600/-ai-security-webinar.jpg\"/></item><item><title>AI
        Adoption in the Enterprise: Breaking Through the Security and Compliance Gridlock</title><description><![CDATA[AI
        holds the promise to revolutionize all sectors of enterprise\u30fcfrom fraud
        detection and content personalization to customer service and security operations.
        Yet, despite its potential, implementation often stalls behind a wall of security,
        legal, and compliance hurdles.\nImagine this all-too-familiar scenario: A
        CISO wants to deploy an AI-driven SOC to handle the overwhelming volume of
        security]]></description><link>https://thehackernews.com/2025/04/ai-adoption-in-enterprise-breaking.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/04/ai-adoption-in-enterprise-breaking.html</guid><pubDate>Thu,
        03 Apr 2025 16:04:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiwQCcQW4EBU0VfJHTvXykserKPJ1bz9dmRqSBvAEBIGXlHlC2gv0yRDztWQ8qUOBNMx3oIA0MAdlFqNV-20OMlTXwQ-EL9Z-AJcHHtVO5KAXe4jCF_RRy36usQ1SLJCe1WZtz1zexdhQ8lxQWN6dS9b6p_ZDacmxsCDnO4YTKJPwDoREBW-SwU-8IJEl8/s1600/ai-security.jpg\"/></item><item><title>Google
        Patches Quick Share Vulnerability Enabling Silent File Transfers Without Consent</title><description><![CDATA[Cybersecurity
        researchers have disclosed details of a new vulnerability impacting Google's
        Quick Share data transfer utility for Windows that could be exploited to achieve
        a denial-of-service (DoS) or send arbitrary files to a target's device without
        their approval.\nThe flaw, tracked as CVE-2024-10668 (CVSS score: 5.9), is
        a bypass for two of the 10 shortcomings that were originally disclosed by]]></description><link>https://thehackernews.com/2025/04/google-patches-quick-share.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/04/google-patches-quick-share.html</guid><pubDate>Thu,
        03 Apr 2025 13:51:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjlZoxvxFaT4TepNFMjnofOlr7j6fVoeRXgT7XHtDFvm3bvnN18jJA6yxLJOd-1sRUPSNpZTo7-1ReJWJ_WVW9p8FS0DmO570e6YqPMPQVc5iloVJqp8RacYYELpQoVZ2SwdxwjZ9SucZ7bhXik5WaqYKPltyQTl6b5IN7PpWuSVV4K7CCR8HhyphenhyphenkJzVklJ0/s1600/quickshare-attack.jpg\"/></item><item><title>Triada
        Malware Preloaded on Counterfeit Android Phones Infects 2,600+ Devices</title><description><![CDATA[Counterfeit
        versions of popular smartphone models that are sold at reduced prices have
        been found to be preloaded with a modified version of an Android malware called
        Triada.\n\"More than 2,600 users in different countries have encountered the
        new version of Triada, the majority in Russia,\" Kaspersky said in a report.
        The infections were recorded between March 13 and 27, 2025.&nbsp;\nTriada
        is the]]></description><link>https://thehackernews.com/2025/04/triada-malware-preloaded-on-counterfeit.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/04/triada-malware-preloaded-on-counterfeit.html</guid><pubDate>Thu,
        03 Apr 2025 13:04:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEj9lQtdkhP6iiKlnwFYB298yo4CfuuQ87avx_KyORFmN8Yt0TAzKCOFdor4Y9BC2Xp9Ag92jTIsWWyw0NINosiLhqtjCgAbPeIss2pnn0mt1h90Ab6Gg5BZ1B5b_A_s0ancfFyR4CVNGaN7U_EufOKYW2DrCJEAmiaf8e8gfVy757Ms68AMNUEaG8WHHxuX/s1600/android-malware.jpg\"/></item><item><title>Legacy
        Stripe API Exploited to Validate Stolen Payment Cards in Web Skimmer Campaign</title><description><![CDATA[Threat
        hunters are warning of a sophisticated web skimmer campaign that leverages
        a legacy application programming interface (API) from payment processor Stripe
        to validate stolen payment information prior to exfiltration.\n\"This tactic
        ensures that only valid card data is sent to the attackers, making the operation
        more efficient and potentially harder to detect,\" Jscrambler researchers
        Pedro]]></description><link>https://thehackernews.com/2025/04/legacy-stripe-api-exploited-to-validate.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/04/legacy-stripe-api-exploited-to-validate.html</guid><pubDate>Thu,
        03 Apr 2025 10:15:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiGKPkCGAcRdk6A5JDQxFjzb0MJnptNLIougw5jjYG0L_h8PELRj371auFqpXF-2DouP6ZyqKWtamj7dMneIG-G0weJCifrvsF-fLIVVx2_rVvCtKHyXEnQ8vnUplzvwJyQej3HXvhTKItI8JoRrKjADM7gcBuh7DEtfmqE98AnnPrtqGAnIKXVCAtCW035/s1600/stripe-skimming.jpg\"/></item><item><title>Europol
        Dismantles Kidflix With 72,000 CSAM Videos Seized in Major Operation</title><description><![CDATA[In
        one of the largest coordinated law enforcement operations, authorities have
        dismantled Kidflix, a streaming platform that offered child sexual abuse material
        (CSAM).\n\"A total of 1.8 million users worldwide logged on to the platform
        between April 2022 and March 2025,\" Europol said in a statement. \"On March
        11, 2025, the server, which contained around 72,000 videos at the time, was
        seized by]]></description><link>https://thehackernews.com/2025/04/europol-dismantles-kidflix-with-72000.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/04/europol-dismantles-kidflix-with-72000.html</guid><pubDate>Thu,
        03 Apr 2025 09:28:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi04ukptBlRS-AOYC-7b_LjWAP1HhMXr7ZX0c-5xOsAriUb4og9_iOYrAmbqEGoMxmOu1gjzxt18ZTlGd2xK4wMQQspWeSfrnyV7wftNTjLA4mW4qHfC1uhu0kfdOmGacDoVbKzDTd6vVfrsMFVq1uM-8chyz-dNU_B7h7AqBsjIB9cdpO5H4cwc4vqeucj/s1600/site.jpg\"/></item><item><title>Google
        Fixed Cloud Run Vulnerability Allowing Unauthorized Image Access via IAM Misuse</title><description><![CDATA[Cybersecurity
        researchers have disclosed details of a now-patched privilege escalation vulnerability
        in Google Cloud Platform (GCP) Cloud Run that could have allowed a malicious
        actor to access container images and even inject malicious code.\n\"The vulnerability
        could have allowed such an identity to abuse its Google Cloud Run revision
        edit permissions in order to pull private Google Artifact]]></description><link>https://thehackernews.com/2025/04/google-fixed-cloud-run-vulnerability.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/04/google-fixed-cloud-run-vulnerability.html</guid><pubDate>Wed,
        02 Apr 2025 19:18:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhXHpZfMK9c_7qs10Nxs5C01t3Rrv9KfcCuKIcVIYr9bKIFY0blX0GW6PaAE9_MIiJiXJLo8O7-djZyzkO7HhG1b60Yr9-u5g_lG2DSPJFTlYeN6pKZOwvfewuy8Gj1RwDe9oeZzB4_RTOOTwvcvPOcCEr5khGOU7rUqbHOin25VbHlpUQmPgeKT8zKan0e/s1600/ImageRunner-vulnerability.gif\"/></item><item><title>Helping
        Your Clients Achieve NIST Compliance: A Step by Step Guide for Service Providers</title><description><![CDATA[Introduction\nAs
        the cybersecurity landscape evolves, service providers play an increasingly
        vital role in safeguarding sensitive data and maintaining compliance with
        industry regulations. The National Institute of Standards and Technology (NIST)
        offers a comprehensive set of frameworks that provide a clear path to achieving
        robust cybersecurity practices.\nFor service providers, adhering to NIST]]></description><link>https://thehackernews.com/2025/04/helping-your-clients-achieve-nist.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/04/helping-your-clients-achieve-nist.html</guid><pubDate>Wed,
        02 Apr 2025 16:55:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjB1D3ky8Wz2VCWya9L1An-rODEsgnofE0_mzsL9A_5Sg6fatoFocDfEcKsCcuQuMJi459oDFcicItUrMLdKqgb1zgzPji7weB2sV_d_wn10B954h4PCJocLnNa0oIndfDJqwkd-h8cdmARmkIAcA5IFJ0vxdYrsj3Ys9FoY1weFMvNzGLvqJsFlVSySvc/s1600/nist.jpg\"/></item><item><title>Outlaw
        Group Uses SSH Brute-Force to Deploy Cryptojacking Malware on Linux Servers</title><description><![CDATA[Cybersecurity
        researchers have shed light on an \"auto-propagating\" cryptocurrency mining
        botnet called Outlaw (aka Dota) that's known for targeting SSH servers with
        weak credentials.\n\"Outlaw is a Linux malware that relies on SSH brute-force
        attacks, cryptocurrency mining, and worm-like propagation to infect and maintain
        control over systems,\" Elastic Security Labs said in a new analysis]]></description><link>https://thehackernews.com/2025/04/outlaw-group-uses-ssh-brute-force-to.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/04/outlaw-group-uses-ssh-brute-force-to.html</guid><pubDate>Wed,
        02 Apr 2025 16:13:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEj3w77_VNhOqHvKMNPiEeri9iIctHc8bg5-8ur61OpsuGsffo7Q-hnwUw4_t2GqYoa5mxzsnNwrNy6p9SYxTzB8kR_jdMmPeJFx3cXhp59uBJdeaJ78ubzbOwsUILyXwL5fuLEP00Qik3z8JzqVWe1I0qheKPQZKBm9SIhP5vBWsQR7W6OZZcjc-vh-EJcS/s1600/linux-malware.jpg\"/></item><item><title>How
        SSL Misconfigurations Impact Your Attack Surface</title><description><![CDATA[When
        assessing an organization\u2019s external attack surface, encryption-related
        issues (especially SSL misconfigurations) receive special attention. Why?
        Their widespread use, configuration complexity, and visibility to attackers
        as well as users make them more likely to be exploited.&nbsp;\nThis highlights
        how important your SSL configurations are in maintaining your web application
        security and]]></description><link>https://thehackernews.com/2025/04/how-ssl-misconfigurations-impact-your.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/04/how-ssl-misconfigurations-impact-your.html</guid><pubDate>Wed,
        02 Apr 2025 15:30:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiECalAu4npkARUJ61hmZv5pyQOZukXmYFwZOf3dX85yncYNPXlNCe0vPYM3JF8QniGP5MeZwVNisMb7yaN6VyGMpJcydN2OhX1gWiShJvnOXY5W3rcychm2pGbaW21micYaOkZmsejRfB_DNwNDtMXpZpXxc831xQmOx9y_YoGlaL-t-RBtQN9SW-x-TM/s1600/outpost-ssl.jpg\"/></item><item><title>FIN7
        Deploys Anubis Backdoor to Hijack Windows Systems via Compromised SharePoint
        Sites</title><description><![CDATA[The financially motivated threat actor
        known as FIN7 has been linked to a Python-based backdoor called Anubis (not
        to be confused with an Android banking trojan of the same name) that can grant
        them remote access to compromised Windows systems.\n\"This malware allows
        attackers to execute remote shell commands and other system operations, giving
        them full control over an infected machine,\" Swiss]]></description><link>https://thehackernews.com/2025/04/fin7-deploys-anubis-backdoor-to-hijack.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/04/fin7-deploys-anubis-backdoor-to-hijack.html</guid><pubDate>Wed,
        02 Apr 2025 12:22:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgg-KAsX8XCyCgqBF_oo56BVgAWPwKG-4OYWMe8uQBZGB-d1BLLFJZW2leNVn1yrL4YxveaxXbZtbE_ufLigj4UW-8JO43muGUSonzxfYIz6BVvGLw9NQ8yLIi7j_puYOUKokhY7uNpi32hPg5bU7GLtEVxIdItCkWlWxDhyoDOi_UCF6EUcc-fWEbwURAV/s1600/windows-hacked.jpg\"/></item><item><title>New
        Malware Loaders Use Call Stack Spoofing, GitHub C2, and .NET Reactor for Stealth</title><description><![CDATA[Cybersecurity
        researchers have discovered an updated version of a malware loader called
        Hijack Loader that implements new features to evade detection and establish
        persistence on compromised systems.\n\"Hijack Loader released a new module
        that implements call stack spoofing to hide the origin of function calls (e.g.,
        API and system calls),\" Zscaler ThreatLabz researcher Muhammed Irfan V A
        said in]]></description><link>https://thehackernews.com/2025/04/new-malware-loaders-use-call-stack.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/04/new-malware-loaders-use-call-stack.html</guid><pubDate>Wed,
        02 Apr 2025 11:25:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgLYn-JbuQeiPM4O4Xk5Cw7fgC9S1VcUkEjkmdJM56HXAunVfBUVZCLgoXOWZVvFdI-E1v6ftVvi7Ip2dw8UmSZRDOSqQJcIzhwKYI2bb2dSk1fIwnzBtfKMK9V1s41fASK1J4KheLbCGrRtmhByJu73K0o2hG_bcFKNKxa12dWI-s-kOA9IG342xvUERQ1/s1600/malware-loader.jpg\"/></item><item><title>Over
        1,500 PostgreSQL Servers Compromised in Fileless Cryptocurrency Mining Campaign</title><description><![CDATA[Exposed
        PostgreSQL instances are the target of an ongoing campaign designed to gain
        unauthorized access and deploy cryptocurrency miners.\nCloud security firm
        Wiz said the activity is a variant of an intrusion set that was first flagged
        by Aqua Security in August 2024 that involved the use of a malware strain
        dubbed PG_MEM. The campaign has been attributed to a threat actor Wiz tracks
        as]]></description><link>https://thehackernews.com/2025/04/over-1500-postgresql-servers.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/04/over-1500-postgresql-servers.html</guid><pubDate>Tue,
        01 Apr 2025 22:38:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi7T76r7kS8PZOsdzi_Rqfb4YQ9TlduBV_oDyqzjBXyrvuLrPjXBthb3OjCYCE8xTnq1h84I8Wfzxt9-v1kK-7lVj1YsxCoxZY8zZIM9knp_wY0_ZAsCQsLz2mUol-4MKoKsTvrZd9W04c39ORJP9qsWlAOeL3a9uhaSaO0cuZ3LC2KRz01mXOTrKxMFccD/s1600/main-crypto.jpg\"/></item><item><title>Enterprise
        Gmail Users Can Now Send End-to-End Encrypted Emails to Any Platform</title><description><![CDATA[On
        the 21st birthday of Gmail, Google has announced a major update that allows
        enterprise users to send end-to-end encrypted (E2EE) to any user in any email
        inbox in a few clicks.\nThe feature is rolling out starting today in beta,
        allowing users to send E2EE emails to Gmail users within an organization,
        with plans to send E2EE emails to any Gmail inbox in the coming weeks and
        to any email inbox]]></description><link>https://thehackernews.com/2025/04/enterprise-gmail-users-can-now-send-end.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/04/enterprise-gmail-users-can-now-send-end.html</guid><pubDate>Tue,
        01 Apr 2025 21:04:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjbxpc3hRdov5Diqy6JBDvzq3Z8vzL4j5F4IoDEur800oUFvl8GJoe6Pd4wgAeworpNX4n8Z2RjKgEkR3G9b4zg4LYrVSUXo_w75oqfTEa0uAYHWLR71cnYgxR3wtBVao50AUMLu56jdNaCafM12WkBUWH0TTp_3H2r1PTSS8dOd_PSEaOG3UXk6IxWCnxE/s1600/gmail-End-to-End-Encrypted.gif\"/></item><item><title>Lucid
        PhaaS Hits 169 Targets in 88 Countries Using iMessage and RCS Smishing</title><description><![CDATA[A
        new sophisticated phishing-as-a-service (PhaaS) platform called Lucid has
        targeted 169 entities in 88 countries using smishing messages propagated via
        Apple iMessage and Rich Communication Services (RCS) for Android.\nLucid's
        unique selling point lies in its weaponizing of legitimate communication platforms
        to sidestep traditional SMS-based detection mechanisms.\n\"Its scalable,]]></description><link>https://thehackernews.com/2025/04/lucid-phaas-hits-169-targets-in-88.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/04/lucid-phaas-hits-169-targets-in-88.html</guid><pubDate>Tue,
        01 Apr 2025 19:48:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgZ-tNebaQQ4zlrOUTWId2atRc-B-_oDKtXIW2pQFT1Xgqh_h_oGvEp-VrziMKj1wmTyh1LLKgxAnqdgSoSXOOJRgsfhFQfNUMB3r_ziK5fT1rSXuFQkZ60PjBCyzmplrygd6GRCN5LyAOjHEEINgikpoqk5zuRtJQojdl7iBxR2UGT89BYeJoH0AcSY2RZ/s1600/sms.jpg\"/></item><item><title>Apple
        Backports Critical Fixes for 3 Recent 0-Days Impacting Older iOS and macOS
        Devices</title><description><![CDATA[Apple on Monday backported fixes for
        three vulnerabilities that have come under active exploitation in the wild
        to older models and previous versions of the operating systems.\nThe vulnerabilities
        in question are listed below -\n\nCVE-2025-24085 (CVSS score: 7.3) - A use-after-free
        bug in the Core Media component that could permit a malicious application
        already installed on a device to elevate]]></description><link>https://thehackernews.com/2025/04/apple-backports-critical-fixes-for-3.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/04/apple-backports-critical-fixes-for-3.html</guid><pubDate>Tue,
        01 Apr 2025 16:58:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiYFkbv9BXSh7qdjOO8CJFYwa1qrHgvlMUAqX1XLjivHW7JU_gKdsNFdX_Z1tXrq-5ZMNgPROgksD1pS3_o3FmAsMeDZEVpr-2y9eXL0zbCNV-ZJaCfCdxv9GeywyfdC8PM1zRe9cHxhFZYuCENi2BahfgYi4ZOHtD9O5pZnpTHkAQFEAmeLUr88D4UDOgq/s1600/ios.jpg\"/></item><item><title>Nearly
        24,000 IPs Target PAN-OS GlobalProtect in Coordinated Login Scan Campaign</title><description><![CDATA[Cybersecurity
        researchers are warning of a spike in suspicious login scanning activity targeting
        Palo Alto Networks PAN-OS GlobalProtect gateways, with nearly 24,000 unique
        IP addresses attempting to access these portals.\n\"This pattern suggests
        a coordinated effort to probe network defenses and identify exposed or vulnerable
        systems, potentially as a precursor to targeted exploitation,\" threat]]></description><link>https://thehackernews.com/2025/04/nearly-24000-ips-target-pan-os.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/04/nearly-24000-ips-target-pan-os.html</guid><pubDate>Tue,
        01 Apr 2025 16:47:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhmbFnFHRVahfGEgdmPP3EiNmei8Y5LXES8k1rTdcEEM24D2x1LNA6qUVztHaj0QddasA5sQ_og2pKN_B7W7v4JG5TpguXlZ9TtvnA1IxWOoPl0ZxE0E-Ergz02j6AWER53xTjHyd46H54q5UCnnfyJjwfN-py1LuqEYB3G2nQUcR9Jp5sEhOnoRop38kTL/s1600/scanning.jpg\"/></item><item><title>Case
        Study: Are CSRF Tokens Sufficient in Preventing CSRF Attacks?</title><description><![CDATA[Explore
        how relying on CSRF tokens as a security measure against CSRF attacks is a
        recommended best practice, but in some cases, they are simply not enough.
        \nIntroduction\nAs per the Open Web Application Security Project (OWASP),
        CSRF vulnerabilities are recognized as a significant threat and are historically
        part of their top risks. The implications of CSRF attacks are far-reaching
        and could]]></description><link>https://thehackernews.com/2025/04/new-case-study-global-retailer.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/04/new-case-study-global-retailer.html</guid><pubDate>Tue,
        01 Apr 2025 16:33:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEghoxZUqr5nrvYoEsgc4PaaERCGSFBXkUv-SQVCd-Q8yoOo5PUhBR6NrEFly2zxlR6sl5BonMQDlplf7mk8LVsc1FNQPvjNm26QGLB30qg2zpxJkVsXthGQoB3jVOKDbGb4KhjMJ5jZresmEmkiAO7nKgYgEYx062hIuykE1061Wc2uDaRBT9eraO-tEd61/s1600/main.jpg\"/></item><item><title>China-Linked
        Earth Alux Uses VARGEIT and COBEACON in Multi-Stage Cyber Intrusions</title><description><![CDATA[Cybersecurity
        researchers have shed light on a new China-linked threat actor called Earth
        Alux that has targeted various key sectors such as government, technology,
        logistics, manufacturing, telecommunications, IT services, and retail in the
        Asia-Pacific (APAC) and Latin American (LATAM) regions.\n\"The first sighting
        of its activity was in the second quarter of 2023; back then, it was]]></description><link>https://thehackernews.com/2025/04/china-linked-earth-alux-uses-vargeit.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/04/china-linked-earth-alux-uses-vargeit.html</guid><pubDate>Tue,
        01 Apr 2025 16:33:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjUg9xRfk-NBs11nqO3ExDvG7lfDaVu27rhVxrpgt0-MSlu6XCY7Z5PcP8MlsUmLe6cgyiMF-0cqKZNslV7olmkb0pI-uvpv35O7OUW2WTxWLVFevrmYh24Aoh8PTz1oeV4UOKm2MGZ9C7RlJ9rK1ijgTElWixp-jS2Lid88IktS1-4f_6xtRzNfzbnfe3Z/s1600/chinese-hackers-attackers.jpg\"/></item><item><title>Apple
        Fined \u20ac150 Million by French Regulator Over Discriminatory ATT Consent
        Practices</title><description><![CDATA[Apple has been hit with a fine of \u20ac150
        million ($162 million) by France's competition watchdog over the implementation
        of its App Tracking Transparency (ATT) privacy framework.\nThe Autorit\xe9
        de la concurrence said it's imposing a financial penalty against Apple for
        abusing its dominant position as a distributor of mobile applications for
        iOS and iPadOS devices between April 26, 2021 and July 25,]]></description><link>https://thehackernews.com/2025/04/apple-fined-150-million-by-french.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/04/apple-fined-150-million-by-french.html</guid><pubDate>Tue,
        01 Apr 2025 11:17:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiY0aRrPaF-m2u0R2UBVOBKUW10naXhHR750hZH7lKXa9LfNyBvS4jQ6DfQ4hrQZ19Tj1g8xNLFkU4RKKKA7Wc2z72h_DiKyZWY7BLqn7QWoQyY1AuPcE_wuemHMcbOGspI-tTEFhN7tSxCBcsZNBYh5VuQHA1ATRwFRjRfQpULZ6JkNltYRspSIOuVvQFM/s1600/apple-fined.jpg\"/></item><item><title>Russian
        Hackers Exploit CVE-2025-26633 via MSC EvilTwin to Deploy SilentPrism and
        DarkWisp</title><description><![CDATA[The threat actors behind the zero-day
        exploitation of a recently-patched security vulnerability in Microsoft Windows
        have been found to deliver two new backdoors called SilentPrism and DarkWisp.\nThe
        activity has been attributed to a suspected Russian hacking group called Water
        Gamayun, which is also known as EncryptHub and LARVA-208.\n\"The threat actor
        deploys payloads primarily by means of]]></description><link>https://thehackernews.com/2025/03/russian-hackers-exploit-cve-2025-26633.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/03/russian-hackers-exploit-cve-2025-26633.html</guid><pubDate>Mon,
        31 Mar 2025 22:11:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEggJa6g8jKzDV-VfotzqyZ5WO-tp1kyFDPHglCvQQAobDG7YbsUkeaeLB-IlqxFysIaIMfeDpmipR_GzW_BWKg3RXjuFheMTgNFh1krGBB_GoQyeajOxttbr2qMqjCDaMqdNrg6iYldX-k6KjR5MyTUwCK-ucJ62_2xpamWvaNzADE9DS-iui-XnYwdW10P/s1600/russian-hackers.jpg\"/></item><item><title>Hackers
        Exploit WordPress mu-Plugins to Inject Spam and Hijack Site Images</title><description><![CDATA[Threat
        actors are using the \"mu-plugins\" directory in WordPress sites to conceal
        malicious code with the goal of maintaining persistent remote access and redirecting
        site visitors to bogus sites.\nmu-plugins, short for must-use plugins, refers
        to plugins in a special directory (\"wp-content/mu-plugins\") that are automatically
        executed by WordPress without the need to enable them explicitly via the]]></description><link>https://thehackernews.com/2025/03/hackers-exploit-wordpress-mu-plugins-to.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/03/hackers-exploit-wordpress-mu-plugins-to.html</guid><pubDate>Mon,
        31 Mar 2025 17:34:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhPGs9FlgRjx323jLr6R1UyNy0lWWISc2edWq4imI_fj-_BJtcrFgd0R10xYSfN2fVkeJ8MqNhCrASXtLqY2uWCPikggp_hMXpRdwltBrTZmmKHIqnXAnyI39VE1XYijoqTZz5sHZ8wc40O1603uoxkgGtayMUg22MrEV30HVjAyB-PpJizNsEORBHOwAFs/s1600/wordpress.jpg\"/></item><item><title>\u26a1
        Weekly Recap: Chrome 0-Day, IngressNightmare, Solar Bugs, DNS Tactics, and
        More</title><description><![CDATA[Every week, someone somewhere slips up\u2014and
        threat actors slip in. A misconfigured setting, an overlooked vulnerability,
        or a too-convenient cloud tool becomes the perfect entry point. But what happens
        when the hunters become the hunted? Or when old malware resurfaces with new
        tricks?\nStep behind the curtain with us this week as we explore breaches
        born from routine oversights\u2014and the unexpected]]></description><link>https://thehackernews.com/2025/03/weekly-recap-chrome-0-day.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/03/weekly-recap-chrome-0-day.html</guid><pubDate>Mon,
        31 Mar 2025 16:55:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgZKCfE5YXei1gHXdzOlHq-QdGJ_ZjbBXcLsABNtCFQM-i5Claor0Vtqytqy-7m6zbwgsZme8V4oMoz5pJUfcne-Pyw-F1sAC-VgOYIQ0aa0sHdPYDXFLjEl5fCI-l1ULmw8wSRTGM63_7evJxpKwGMmnXHParuDI5QuUnaWgkpxKuFrCW2FSb3rrNMze83/s1600/recap.jpg\"/></item><item><title>5
        Impactful AWS Vulnerabilities You're Responsible For</title><description><![CDATA[If
        you're using AWS, it's easy to assume your cloud security is handled - but
        that's a dangerous misconception. AWS secures its own infrastructure, but
        security within a cloud environment remains the customer\u2019s responsibility.\nThink
        of AWS security like protecting a building: AWS provides strong walls and
        a solid roof, but it's up to the customer to handle the locks, install the
        alarm systems,]]></description><link>https://thehackernews.com/2025/03/5-impactful-aws-vulnerabilities-youre.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/03/5-impactful-aws-vulnerabilities-youre.html</guid><pubDate>Mon,
        31 Mar 2025 16:30:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiq_6t9LdSXCel6_VWE7MK8aOrWpCzpgP0OTAgDxgQMfJTzfx4MY_J60-p4R9fWgnSSscBBniRZkoUz-yocolV2xcXsSQWXeBnnBgNXFb5EfbgrmrWcgasgeEco6ZkXHE5fludN4VlBV_0bzpkh78c9xJeZjOkE23ZSk3T30vg9OKF-voyogFeJqbA0TCk/s1600/aws.jpg\"/></item><item><title>Russia-Linked
        Gamaredon Uses Troop-Related Lures to Deploy Remcos RAT in Ukraine</title><description><![CDATA[Entities
        in Ukraine have been targeted as part of a phishing campaign designed to distribute
        a remote access trojan called Remcos RAT.\n\"The file names use Russian words
        related to the movement of troops in Ukraine as a lure,\" Cisco Talos researcher
        Guilherme Venere said in a report published last week. \"The PowerShell downloader
        contacts geo-fenced servers located in Russia and Germany to]]></description><link>https://thehackernews.com/2025/03/russia-linked-gamaredon-uses-troop.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/03/russia-linked-gamaredon-uses-troop.html</guid><pubDate>Mon,
        31 Mar 2025 15:00:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhlN25sawOUlcNHvf04i5rlGONwvvllYqkvd0GqPZ82VVgViJpmdRoTfA2wU5GTH2DcrHtCrkiiQEWlKXSLFdo-yzAXOCzCN5vhICXeWoP6XSOAMXOHgcjTrzp6qaIG9_aIUOKxFr7U4iMD_riq5k9MoeAJAMUCNkig5SCN_x8aS0_J8sqRiej98AhXN6XD/s1600/phishing-malware.jpg\"/></item><item><title>RESURGE
        Malware Exploits Ivanti Flaw with Rootkit and Web Shell Features</title><description><![CDATA[The
        U.S. Cybersecurity and Infrastructure Security Agency (CISA) has shed light
        on a new malware called RESURGE that has been deployed as part of exploitation
        activity targeting a now-patched security flaw in Ivanti Connect Secure (ICS)
        appliances.\n\"RESURGE contains capabilities of the SPAWNCHIMERA malware variant,
        including surviving reboots; however, RESURGE contains distinctive commands
        that]]></description><link>https://thehackernews.com/2025/03/resurge-malware-exploits-ivanti-flaw.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/03/resurge-malware-exploits-ivanti-flaw.html</guid><pubDate>Sun,
        30 Mar 2025 10:37:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjkhyphenhypheneoW69oCkjaVurSbaYCsIEwZ-_mdd2ynA_V9eVIDOIfhFIUZpULKbiIvM1AfnbRxNqLgGijgZXTEuV41rCkIhsZK6Z2xJeRiWaEGW2L4JRzdXpeeAiEA4NW_gmIZmm1sRf7zsfVV27MOy15tggcIZvr-OgxGASbbt_VgkKks2V4rw4S3GpdELrnmv5q/s1600/malware-attack.jpg\"/></item><item><title>New
        Android Trojan Crocodilus Abuses Accessibility to Steal Banking and Crypto
        Credentials</title><description><![CDATA[Cybersecurity researchers have discovered
        a new Android banking malware called Crocodilus that's primarily designed
        to target users in Spain and Turkey.\n\"Crocodilus enters the scene not as
        a simple clone, but as a fully-fledged threat from the outset, equipped with
        modern techniques such as remote control, black screen overlays, and advanced
        data harvesting via accessibility logging,\"]]></description><link>https://thehackernews.com/2025/03/new-android-trojan-crocodilus-abuses.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/03/new-android-trojan-crocodilus-abuses.html</guid><pubDate>Sat,
        29 Mar 2025 12:58:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEir2MTEFBnBDvG1HzYB810kGKLnr_RhL7Bl6lFHdsrlEMWPuG8LyZkinSppjn9D7H9ReyqIbmt-sGaaHSCTSzlpBoLLw-IZ-JtcCLflvhcX2O-E6Ae9Rff4N6Q9TceCnCt6gShjRdrhd74HyZZLB3129HDTlBy_9EhMRhEvukH3yil8xBI9Xtw0EILxYWU7/s1600/trojan.jpg\"/></item><item><title>BlackLock
        Ransomware Exposed After Researchers Exploit Leak Site Vulnerability</title><description><![CDATA[In
        what's an instance of hacking the hackers, threat hunters have managed to
        infiltrate the online infrastructure associated with a ransomware group called
        BlackLock, uncovering crucial information about their modus operandi in the
        process. \nResecurity said it identified a security vulnerability in the data
        leak site (DLS) operated by the e-crime group that made it possible to extract]]></description><link>https://thehackernews.com/2025/03/blacklock-ransomware-exposed-after.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/03/blacklock-ransomware-exposed-after.html</guid><pubDate>Sat,
        29 Mar 2025 09:22:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgBX2w2b0OU8NYSPW4qNsxebC6yXcxsAi0SMAuj5F_R53I4o9ORaUwOtsukdZAU5HsYAeOp0dR4LB96QQ4QQhshx9uUuhmrcWCa1gk6cT1Bpoa8oozYeY0eEh8V9YZAAJZgOD4ko4kk8Ix6DFH-YEgdTexJdIWBuaPK0XO9zSyam9VVQpkZGYVZUkA0Eknt/s1600/malware-ransomware.jpg\"/></item><item><title>Researchers
        Uncover 46 Critical Flaws in Solar Power Systems From Sungrow, Growatt, and
        SMA</title><description><![CDATA[Cybersecurity researchers have disclosed
        46 new security flaws in products from three solar power system vendors, Sungrow,
        Growatt, and SMA, that could be exploited by a bad actor to seize control
        of devices or execute code remotely, posing severe risks to electrical grids.&nbsp;\nThe
        vulnerabilities have been collectively codenamed SUN:DOWN by Forescout Vedere
        Labs.\n\"The new vulnerabilities can]]></description><link>https://thehackernews.com/2025/03/researchers-uncover-46-critical-flaws.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/03/researchers-uncover-46-critical-flaws.html</guid><pubDate>Fri,
        28 Mar 2025 18:51:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhFyI_LQ-MqCu7UZv-PHIqZt71kMhyphenhyphen-9MTEeRCIxbJOgzt2U4YrwPwhwDBMUdEi8BJ4015syM8dEGRV2kITLEkRxXkPeut6QDWjkOXBsSsepsThJE_Njq2Evt68RObgzYeQcswbxHOHbYrrJYqZpEXYFGsPWCVaEN4oh4hjK4rzCkz4hHBBmTrTYI03usQg/s1600/hacking.jpg\"/></item><item><title>CoffeeLoader
        Uses GPU-Based Armoury Packer to Evade EDR and Antivirus Detection</title><description><![CDATA[Cybersecurity
        researchers are calling attention to a new sophisticated malware called CoffeeLoader
        that's designed to download and execute secondary payloads.\nThe malware,
        according to Zscaler ThreatLabz, shares behavioral similarities with another
        known malware loader known as SmokeLoader.&nbsp;\n\"The purpose of the malware
        is to download and execute second-stage payloads while evading]]></description><link>https://thehackernews.com/2025/03/coffeeloader-uses-gpu-based-armoury.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/03/coffeeloader-uses-gpu-based-armoury.html</guid><pubDate>Fri,
        28 Mar 2025 17:27:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEh2fYLhTNb5otODcligdkCAf7vEAZYlvB5Rbu4eRfpCaEIv2FtcVWt_uU172aUuf15LJIrx_B90UxgF0HH-DcqEAFijDDfQ7Q8OsIJQFS7koTIJZjewr1ffcHhzWRfToQvU8qE19WAoeWOyzmh-EsFGS16v_6xCrXwlBZ_US-ZVwJat1AVhXv4f6MMzoOJW/s1600/malware.png\"/></item><item><title>Product
        Walkthrough: How Datto BCDR Delivers Unstoppable Business Continuity</title><description><![CDATA[Long
        gone are the days when a simple backup in a data center was enough to keep
        a business secure. While backups store information, they do not guarantee
        business continuity during a crisis. With IT disasters far too common and
        downtime burning through budgets, modern IT environments require solutions
        that go beyond storage and enable instant recovery to minimize downtime and
        data loss. This is]]></description><link>https://thehackernews.com/2025/03/how-to-ensure-business-continuity-with-datto-b.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/03/how-to-ensure-business-continuity-with-datto-b.html</guid><pubDate>Fri,
        28 Mar 2025 15:45:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjcJh4q5lSFB_BO0Th8HO3KKRr9uZOx04wBI3xzlwiOvTbcbZ7SDXcTDKfvtMdblJdiKSj-RMdjEVEOsdeXX6aSbALJQXtBfGw4GJQaS4ADZk9rkQ3F0BCdS_zD1CDf2B4iSODBrDldRfoPJ7dmZeG9D6hdLfKhqG2NdMxIMPxz0N6v4LrzQeuEhopiSBw/s1600/dat-main.jpg\"/></item><item><title>PJobRAT
        Malware Campaign Targeted Taiwanese Users via Fake Chat Apps</title><description><![CDATA[An
        Android malware family previously observed targeting Indian military personnel
        has been linked to a new campaign likely aimed at users in Taiwan under the
        guise of chat apps.\n\"PJobRAT can steal SMS messages, phone contacts, device
        and app information, documents, and media files from infected Android devices,\"
        Sophos security researcher Pankaj Kohli said in a Thursday analysis.\nPJobRAT,
        first]]></description><link>https://thehackernews.com/2025/03/pjobrat-malware-campaign-targeted.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/03/pjobrat-malware-campaign-targeted.html</guid><pubDate>Fri,
        28 Mar 2025 13:36:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgqxS100V1iLV4XtqrbMO4tYNdGGvaR4kE8i-9b_9tQDwxpCTpV0S48VdgwcmQnVW6gLZTIuGcrzUAkQQPwa3U7gY3wIW46YHq9jh8D9vg8A80_B2b-LkCY4CQbnsAPTmprv7EKsGTElfs4I4KRoXXlkjhslBFq3F0bKL82J3yLwC1vWQ9tuTPlhThmlcwF/s1600/spyware.jpg\"/></item><item><title>Nine-Year-Old
        npm Packages Hijacked to Exfiltrate API Keys via Obfuscated Scripts</title><description><![CDATA[Cybersecurity
        researchers have discovered several cryptocurrency packages on the npm registry
        that have been hijacked to siphon sensitive information such as environment
        variables from compromised systems.\n\"Some of these packages have lived on
        npmjs.com for over 9 years, and provide legitimate functionality to blockchain
        developers,\" Sonatype researcher Ax Sharma said. \"However, [...] the latest]]></description><link>https://thehackernews.com/2025/03/nine-year-old-npm-packages-hijacked-to.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/03/nine-year-old-npm-packages-hijacked-to.html</guid><pubDate>Fri,
        28 Mar 2025 11:36:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhRHyI7MCx5PPlx-4RJmmZ_JjNm0HjuU6dH_Qz9Y57-YDLO1T2dhmhyntIMJD9xLOgqaTyCk9VuHf7LTr7zubqnyMTCX-Ni2-GCsa_umDhc2BM8k2ER-jBiEp9xFAxYG_WGzdD8TAtA9MIgCcgTxsIG7Xg8weHTbNmTNOoFxvKT7aj2KITBArHEwpyTI1pW/s1600/npm-malware.jpg\"/></item><item><title>Mozilla
        Patches Critical Firefox Bug Similar to Chrome\u2019s Recent Zero-Day Vulnerability</title><description><![CDATA[Mozilla
        has released updates to address a critical security flaw impacting its Firefox
        browser for Windows, merely days after Google patched a similar flaw in Chrome
        that came under active exploitation as a zero-day.\nThe security vulnerability,
        CVE-2025-2857, has been described as a case of an incorrect handle that could
        lead to a sandbox escape.\n\"Following the recent Chrome sandbox escape (]]></description><link>https://thehackernews.com/2025/03/mozilla-patches-critical-firefox-bug.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/03/mozilla-patches-critical-firefox-bug.html</guid><pubDate>Fri,
        28 Mar 2025 11:14:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi5x0gk19bEnnDT4C5ZxgV1ih2o8uGpXZNhez0idrDLoV7Hx5Z0Iv68cu4Wf-5Zmj-eKwR_BlTLwETxsv4iOxhflrO0GA7lbxnKspHZVoUxTztcmhIxVjPPyMpSQgP5TOYhzZbuycNhpI8LOvX07gvoNTFWy2J1ZdBkmoS7iaIVBcjWza34EDVOLH4WIA5o/s1600/firefox.jpg\"/></item><item><title>New
        Morphing Meerkat Phishing Kit Mimics 114 Brands Using Victims\u2019 DNS Email
        Records</title><description><![CDATA[Cybersecurity researchers have shed light
        on a new phishing-as-a-service (PhaaS) platform that leverages the Domain
        Name System (DNS) mail exchange (MX) records to serve fake login pages that
        impersonate about 114 brands.\nDNS intelligence firm Infoblox is tracking
        the actor behind the PhaaS, the phishing kit, and the related activity under
        the moniker Morphing Meerkat.\n\"The threat actor behind]]></description><link>https://thehackernews.com/2025/03/new-morphing-meerkat-phishing-kit.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/03/new-morphing-meerkat-phishing-kit.html</guid><pubDate>Thu,
        27 Mar 2025 22:28:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjJNSEzU8vpxLt5F5nrz672X1QUhKXN6BIcnDulfqBA8OEFaaNB-QjGMiGnJqd9Av7FwIEVzONWwgyALXxaeTRwvf6BScmYXy0aqg3EWbMN1MTNg-NCehT_SU1MOZ6DzQL6b5bTQkPz-SF7Omufjh2yMc966xneNQu2rvVtYZrPo0NgGq7gQYyM8YEXbq7U/s1600/phishing.jpg\"/></item><item><title>Hackers
        Repurpose RansomHub's EDRKillShifter in Medusa, BianLian, and Play Attacks</title><description><![CDATA[A
        new analysis has uncovered connections between affiliates of RansomHub and
        other ransomware groups like Medusa, BianLian, and Play.\nThe connection stems
        from the use of a custom tool that's designed to disable endpoint detection
        and response (EDR) software on compromised hosts, according to ESET. The EDR
        killing tool, dubbed EDRKillShifter, was first documented as used by RansomHub
        actors in]]></description><link>https://thehackernews.com/2025/03/hackers-repurpose-ransomhubs.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/03/hackers-repurpose-ransomhubs.html</guid><pubDate>Thu,
        27 Mar 2025 19:40:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEj4Ap5Ps7ihRQT2KJVM15elZd5cCJZ0ip2d0Ug4I8zuHMhHCCkEWbjB63xxoQ2uDr-cQN7iS08YQO9pRgnlYAuW0SZGf3IKpMrByYxUcIXok3lfEKO_9uoO5IT6F_XIZ0I_dbdcJn8hIN-kal5cdg8wHCBGVRZ5RxgxAf-Df-7vYie6lodYCSuUBVjE1oF0/s1600/hackers.png\"/></item><item><title>APT36
        Spoofs India Post Website to Infect Windows and Android Users with Malware</title><description><![CDATA[An
        advanced persistent threat (APT) group with ties to Pakistan has been attributed
        to the creation of a fake website masquerading as India's public sector postal
        system as part of a campaign designed to infect both Windows and Android users
        in the country.\nCybersecurity company CYFIRMA has attributed the campaign
        with medium confidence to a threat actor called APT36, which is also known
        as]]></description><link>https://thehackernews.com/2025/03/apt36-spoofs-india-post-website-to.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/03/apt36-spoofs-india-post-website-to.html</guid><pubDate>Thu,
        27 Mar 2025 18:01:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjyxDLEuZOVO7NZTXa5Mq7qdBqdTNQhPGAwACTjJr13id2au8eFEd3s8SbJ-mJGO1R3dE6QFbiD9ZqNEg17gd5yFKFhsOgrnH2Ryp7gDtxIPiyumw8O3fRtKtw77eWAbj7YDtQF7ibJG4tXAu4gVUmpt1FeEEx3kkPmHoF4v8EQexNUeKp50rJgaK478fc7/s1600/malware-attack.png\"/></item><item><title>New
        Report Explains Why CASB Solutions Fail to Address Shadow SaaS and How\\_to\\_Fix\\_It</title><description><![CDATA[Whether
        it\u2019s CRMs, project management tools, payment processors, or lead management
        tools - your workforce is using SaaS applications by the pound. Organizations
        often rely on traditional CASB solutions for protecting against malicious
        access and data exfiltration, but these fall short for protecting against
        shadow SaaS, data damage, and more.\nA new report, Understanding SaaS Security
        Risks: Why]]></description><link>https://thehackernews.com/2025/03/new-report-explains-why-casb-solutions.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/03/new-report-explains-why-casb-solutions.html</guid><pubDate>Thu,
        27 Mar 2025 16:55:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiYiS1gzqvdwdi1YtF0UO1kwBbS-_aNdUs1Yq9wbsfzOK5InSdCaWHgfZxGD3JYCHCedzfrwljXA7tmhZPPitPhiIvEuLp9PapRJvQbsAIEhBdYEwEGPzVoIc7AoIc__sppk9DlmE9A1BUfzAgbvZV7JezLdCoZFTzG1aSGlOcZSasO3j3NVV7nKBzfkD8/s1600/browser-security.png\"/></item><item><title>Top
        3 MS Office Exploits Hackers Use in 2025 \u2013 Stay Alert!</title><description><![CDATA[Hackers
        have long used Word and Excel documents as delivery vehicles for malware,
        and in 2025, these tricks are far from outdated. From phishing schemes to
        zero-click exploits, malicious Office files are still one of the easiest ways
        into a victim\u2019s system.\nHere are the top three Microsoft Office-based
        exploits still making the rounds this year and what you need to know to avoid
        them.\n1.]]></description><link>https://thehackernews.com/2025/03/top-3-ms-office-exploits-hackers-use-in.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/03/top-3-ms-office-exploits-hackers-use-in.html</guid><pubDate>Thu,
        27 Mar 2025 15:30:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgiGMxa8yBpzRfFEFuvf_fz4wIHrqZhi5a8wLHK-tbs6VDGhTZicQuGjsn39I9B-U2yHcsmKaFwWYD4oJKk_T3w62c2mP1X5piBw-HcJQ7feoh9b8gJaciCQd56Q4aE9_NHYSs-c6BxNw7nV_MGtdpCRwAsTGVUt8y49Xkr4OMfi_3I7zFAWPXQHsDVkNOv/s1600/ms-exploit.png\"/></item><item><title>150,000
        Sites Compromised by JavaScript Injection Promoting Chinese Gambling Platforms</title><description><![CDATA[An
        ongoing campaign that infiltrates legitimate websites with malicious JavaScript
        injects to promote Chinese-language gambling platforms has ballooned to compromise
        approximately 150,000 sites to date.\n\"The threat actor has slightly revamped
        their interface but is still relying on an iframe injection to display a full-screen
        overlay in the visitor's browser,\" c/side security analyst Himanshu]]></description><link>https://thehackernews.com/2025/03/150000-sites-compromised-by-javascript.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/03/150000-sites-compromised-by-javascript.html</guid><pubDate>Thu,
        27 Mar 2025 13:43:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjPfB5mSzg_6S-jTRJW-MG7KMYEcMcEAdsFjXOHnQJjQ4PTShcgNiCXvosCGyxZXGi1Y-xZWj2RIhF-CDnd-A_uKh8p9dVoPx1T0FQO7UzCGzG5FbVt374TjIQExJP5ARL7fWh2zB6u_2c5NimPrsVe-tP5CU1ARlku89VTWQbj9LTQxdFCRfqO1s55xck4/s1600/chinese-hackers.png\"/></item><item><title>CISA
        Warns of Sitecore RCE Flaws; Active Exploits Hit Next.js and DrayTek Devices</title><description><![CDATA[The
        U.S. Cybersecurity and Infrastructure Security Agency (CISA) has added two
        six-year-old security flaws impacting Sitecore CMS and Experience Platform
        (XP) to its Known Exploited Vulnerabilities (KEV) catalog, based on evidence
        of active exploitation.\nThe vulnerabilities are listed below -\n\nCVE-2019-9874
        (CVSS score: 9.8) - A deserialization vulnerability in the Sitecore.Security.AntiCSRF]]></description><link>https://thehackernews.com/2025/03/cisa-flags-two-six-year-old-sitecore.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/03/cisa-flags-two-six-year-old-sitecore.html</guid><pubDate>Thu,
        27 Mar 2025 11:53:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiI1j3HrVjGIlv1z4x_VaWAEUGeMurZSzFYJvS0cVnI11C4LKtju0XpiPw-zjQzzpm7wq0zgvdYimX8oJr95f4asFOqc3s8yIQJrLevOcd_u0L1-xNfAhs6EWvH7fEZ8dagOn1yF6O1NuTH88GwlQaLriyHD3KLik-1eK_ntMAobutloDET8Qu4zSD68nR-/s1600/cisa.png\"/></item><item><title>NetApp
        SnapCenter Flaw Could Let Users Gain Remote Admin Access on Plug-In Systems</title><description><![CDATA[A
        critical security flaw has been disclosed in NetApp SnapCenter that, if successfully
        exploited, could allow privilege escalation.\nSnapCenter is an enterprise-focused
        software that's used to manage data protection across applications, databases,
        virtual machines, and file systems, offering the ability to backup, restore,
        and clone data resources.\n\nThe vulnerability, tracked as]]></description><link>https://thehackernews.com/2025/03/netapp-snapcenter-flaw-could-let-users.html</link><guid
        isPermaLink=\"false\">https://thehackernews.com/2025/03/netapp-snapcenter-flaw-could-let-users.html</guid><pubDate>Thu,
        27 Mar 2025 11:36:00 +0530</pubDate><author>info@thehackernews.com (The Hacker
        News)</author><enclosure length=\"12216320\" type=\"image/jpeg\" url=\"https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgKMKtzk02rkDZJlwJU6wTHXvkEYmy2hjopedjEVjzyB34vbWcRd-mp1k0hsJlLm6fQbwqCyo0OQwVRG7ydWqIDCzti69gBup87_Hu4Y4IgMuTfTqbWaMFQTKyZ4ErgAUxK3ywLmQ_jC2pKFASP7_Vkf27-JBE6TBM5OCSwtIaqTI0oBxxRkpJtcKZwK14-/s1600/hacker.png\"/></item></channel></rss>"""


@pytest.fixture
def thn_news(thn_xml: str) -> ArticlesList:
    articles = TheHackerNewsSource()._xml_to_list_of_articles(thn_xml)
    return ArticlesList(articles=articles)


@pytest.fixture
def test_prompt() -> str:
    prompt = """
                    I'm in software development. Given text with cybersecurity news,
                    extract only new CVEs and vulnerabilities that:
                    Affect Python/TypeScript frameworks, web/cloud apps, Android/iOS
                    Have known vulnerable versions
                    Exclude malware, actors, campaigns
                    Use only listed tech, make no assumptions
                    Must meet all criteria, use only text content
                  """
    return prompt


@contextmanager
def patch_config_file(content: str = "", exists: bool = True) -> Iterator[Any]:
    with patch("pathlib.Path.read_text") as m_content, patch("pathlib.Path.exists") as m_exists:
        m_content.return_value = content
        m_exists.return_value = exists
        yield m_content
