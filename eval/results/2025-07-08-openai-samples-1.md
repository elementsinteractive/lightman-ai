
# Summary
- Tag: -
- Agent: openai
- Samples: 1
- Score threshold: 8
- Prompt: 
 I'm in software development. I develop web applications and mobile applications.
Given a text with cybersecurity news,
Give a score 1-10 to each one of all the articles, depending on how relevant they are to me. Give me back the articles with the relevance that you think they have.
The criteria to follow is:
- I develop with Python, javascript, AWS, android and ios. Also show vulnerabilities about other cloud providers that are directly related with development.
- I'm not interested in libraries vulnerabilities when they are impersonating a legit library, consider them as malware. I'm interested in vulnerabilities of legit libraries when they are critical.
- Even if it's a vulnerability related with development but does not belong to the techonolgies that I'm interested in, it is not relevant for me.
- I'm not interested in malware related news, nor malware campaigns or hackers exploiting vulnerabilities or rootkits using already known vulnerabilities. I'm interested only in newly discovered vulnerabilities.
- I'm only interested in the following mobile brands when it comes to hardware mobile vulnerabilities: Google, Apple, Samsung, Oppo, Motorola, OnePlus, Sony, Lenovo, OPPO, Huawei, Oneplus, Acer, Asus, Nokia, LG, HTC
- I deploy using docker containers, with linux images.
- I'm interested in browsers vulnerabilities.
- I usually use postgresql as a DB, but I'm also interested on other major DB vendors that are commonly used along with the technologies I've mentioned.

very important:
- Make a distinction between exploits and vulnerabilities being exploited and newly discovered vulnerabilities.
- Articles not related to the technologies I use are not relevant for me.



- Average Recall: 0.83, 95% CI: [NaN, NaN]
- Average Precision: 1.00, 95% CI: [NaN, NaN]
- Average Time Delta: 11.02s
- Average F1 Score: 0.91

# Individual sample results

## Result 1
- Total relevant articles: 6
- Total articles found by AI agent: 5
- Total relevant articles found: 5
- Total false positives: 0
- Total false negatives: 1
- Recall: 0.83
- Precision: 1.00
- Time delta: 11.02s

## Articles found by AI agent:
- Qualcomm Fixes 3 Zero-Days Used in Targeted Android Attacks via Adreno GPU
- New Linux Flaws Allow Password Hash Theft via Core Dumps in Ubuntu, RHEL, Fedora
- New Chrome Vulnerability Enables Cross-Origin Data Leak via Loader Referrer Policy
- New Chrome Zero-Day Actively Exploited; Google Issues Emergency Out-of-Band Patch
- PostgreSQL Vulnerability Exploited Alongside BeyondTrust Zero-Day in Targeted Attacks

## Correctly classified articles:
- Title: Qualcomm Fixes 3 Zero-Days Used in Targeted Android Attacks via Adreno GPU
	- Reason: Zero-day vulnerabilities in Qualcomm Adreno GPUs directly affect Android mobile development, especially for devices from major manufacturers. These are high-severity new vulnerabilities (CVSS 8.6), not exploits of known ones.
	- Score: 9
- Title: New Linux Flaws Allow Password Hash Theft via Core Dumps in Ubuntu, RHEL, Fedora
	- Reason: Linux vulnerabilities (specifically Ubuntu, RHEL, and Fedora) are highly relevant if you deploy with Docker and use Linux images. New vulnerabilities in core dump handlers can affect the security of containerized deployments.
	- Score: 8
- Title: New Chrome Vulnerability Enables Cross-Origin Data Leak via Loader Referrer Policy
	- Reason: Newly discovered Chrome browser vulnerabilities are highly relevant for web and mobile developers, particularly when they involve JavaScript and cross-origin policies.
	- Score: 9
- Title: New Chrome Zero-Day Actively Exploited; Google Issues Emergency Out-of-Band Patch
	- Reason: A new Chrome zero-day in the V8 JavaScript/WebAssembly engine is highly relevant due to your use of JavaScript and browser technologies. This is a newly found, actively exploited vulnerability.
	- Score: 10
- Title: PostgreSQL Vulnerability Exploited Alongside BeyondTrust Zero-Day in Targeted Attacks
	- Reason: A previously unknown SQL injection flaw in PostgreSQL (CVE-2025-1094) directly affects a database you use. This is a new vulnerability, not just an exploit of a known one.
	- Score: 10

## False positives:
No results.

## False negatives:
- Title: Microsoft Fixes 78 Flaws, 5 Zero-Days Exploited; CVSS 10 Bug Impacts Azure DevOps Server
	- Reason: MISSED ARTICLE!. This article was not returned by the AI!
	- Score: 1
