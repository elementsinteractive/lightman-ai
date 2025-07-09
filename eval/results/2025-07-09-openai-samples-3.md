
# Summary
- Tag: -
- Agent: openai
- Samples: 3
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



- Average Recall: 0.94, 95% CI: [0.70, 1.00]
- Average Precision: 0.77, 95% CI: [0.58, 0.97]
- Average Time Delta: 31.27s
- Average F1 Score: 0.85

# Individual sample results

## Result 1
- Total relevant articles: 6
- Total articles found by AI agent: 7
- Total relevant articles found: 6
- Total false positives: 1
- Total false negatives: 0
- Recall: 1.00
- Precision: 0.86
- Time delta: 22.46s

## Articles found by AI agent:
- PostgreSQL Vulnerability Exploited Alongside BeyondTrust Zero-Day in Targeted Attacks
- New Chrome Vulnerability Enables Cross-Origin Data Leak via Loader Referrer Policy
- New Chrome Zero-Day Actively Exploited; Google Issues Emergency Out-of-Band Patch
- Microsoft Fixes 78 Flaws, 5 Zero-Days Exploited; CVSS 10 Bug Impacts Azure DevOps Server
- Samsung Patches CVE-2025-4632 Used to Deploy Mirai Botnet via MagicINFO 9 Exploit
- New Linux Flaws Allow Password Hash Theft via Core Dumps in Ubuntu, RHEL, Fedora
- Qualcomm Fixes 3 Zero-Days Used in Targeted Android Attacks via Adreno GPU

## Correctly classified articles:
- Title: Microsoft Fixes 78 Flaws, 5 Zero-Days Exploited; CVSS 10 Bug Impacts Azure DevOps Server
	- Reason: Among Microsoft's reported vulnerabilities, there's a CVSS 10.0 critical bug impacting Azure DevOps Server. If you use Azure DevOps or integrate with Azure in your CI/CD or project workflows, this is highly relevant, especially for development environments.
	- Score: 8
- Title: New Linux Flaws Allow Password Hash Theft via Core Dumps in Ubuntu, RHEL, Fedora
	- Reason: Race condition vulnerabilities in apport and systemd-coredump for Ubuntu, RHEL, and Fedora allow sensitive info leakage. As you deploy using Docker containers with Linux images, this flaw is critical for both production and development environments.
	- Score: 9
- Title: Qualcomm Fixes 3 Zero-Days Used in Targeted Android Attacks via Adreno GPU
	- Reason: Three newly discovered zero-days (CVE-2025-21479/21480/21481) in Qualcomm Adreno GPU (Android) have been exploited in the wild. If you develop Android applications, especially for devices using Qualcomm chips (Google, Samsung, etc.), these vulnerabilities are critical.
	- Score: 10
- Title: PostgreSQL Vulnerability Exploited Alongside BeyondTrust Zero-Day in Targeted Attacks
	- Reason: This article discusses a newly discovered SQL injection flaw (CVE-2025-1094) in PostgreSQL's interactive tool, which is highly relevant if you use PostgreSQL as a database in your projects. The vulnerability is critical (CVSS 8.1) and could impact your development and production environments.
	- Score: 10
- Title: New Chrome Vulnerability Enables Cross-Origin Data Leak via Loader Referrer Policy
	- Reason: This describes a newly discovered high-severity vulnerability (CVE-2025-4664) in Google Chrome that enables cross-origin data leaks. As a web and mobile developer, browser vulnerabilities can affect your apps’ security, especially those using OAuth or cookies for authentication.
	- Score: 9
- Title: New Chrome Zero-Day Actively Exploited; Google Issues Emergency Out-of-Band Patch
	- Reason: A critical, newly discovered Chrome browser zero-day (CVE-2025-5419, V8 JavaScript/WebAssembly engine), with an emergency patch released by Google. This is crucial for both web and mobile development as it could be exploited through your app’s browser contexts or embedded webviews.
	- Score: 10

## False positives:
- Title: Samsung Patches CVE-2025-4632 Used to Deploy Mirai Botnet via MagicINFO 9 Exploit
	- Reason: A newly patched critical path traversal vulnerability (CVSS 9.8) in Samsung MagicINFO 9 Server, used in live attacks. If you develop for Samsung smart devices or manage Docker/Linux-based infrastructure that might use this software, this is very relevant.
	- Score: 8

## False negatives:
No results.



## Result 2
- Total relevant articles: 6
- Total articles found by AI agent: 9
- Total relevant articles found: 6
- Total false positives: 2
- Total false negatives: 0
- Recall: 1.00
- Precision: 0.75
- Time delta: 28.11s

## Articles found by AI agent:
- Microsoft Fixes 78 Flaws, 5 Zero-Days Exploited; CVSS 10 Bug Impacts Azure DevOps Server
- New Linux Flaws Allow Password Hash Theft via Core Dumps in Ubuntu, RHEL, Fedora
- Qualcomm Fixes 3 Zero-Days Used in Targeted Android Attacks via Adreno GPU
- PostgreSQL Vulnerability Exploited Alongside BeyondTrust Zero-Day in Targeted Attacks
- New Chrome Vulnerability Enables Cross-Origin Data Leak via Loader Referrer Policy
- New Chrome Zero-Day Actively Exploited; Google Issues Emergency Out-of-Band Patch
- Commvault Confirms Hackers Exploited CVE-2025-3928 as Zero-Day in Azure Breach
- New Linux Flaws Allow Password Hash Theft via Core Dumps in Ubuntu, RHEL, Fedora
- Microsoft OneDrive File Picker Flaw Grants Apps Full Cloud Access — Even When Uploading Just One File

## Correctly classified articles:
- Title: Microsoft Fixes 78 Flaws, 5 Zero-Days Exploited; CVSS 10 Bug Impacts Azure DevOps Server
	- Reason: Addresses newly discovered vulnerabilities in Azure DevOps Server and Microsoft ecosystem. Includes CVSS 10 cloud bug relevant for developers using Azure and possibly broader impacts for CI/CD pipelines or integrations seen in web/mobile app workflows.
	- Score: 8
- Title: New Linux Flaws Allow Password Hash Theft via Core Dumps in Ubuntu, RHEL, Fedora
	- Reason: Newly discovered vulnerabilities in key Linux distributions used as Docker image bases (Ubuntu, RHEL, Fedora). Risk is relevant due to local privilege concerns on server or developer containers.
	- Score: 8
- Title: Qualcomm Fixes 3 Zero-Days Used in Targeted Android Attacks via Adreno GPU
	- Reason: Critical zero-days affecting Android devices (hardware vendors like Samsung, Google, OnePlus, etc. use Qualcomm chips). Direct impact for mobile application developers concerned about device-level vulnerabilities.
	- Score: 9
- Title: PostgreSQL Vulnerability Exploited Alongside BeyondTrust Zero-Day in Targeted Attacks
	- Reason: Newly discovered critical SQL injection vulnerability in PostgreSQL ('psql' tool). Directly impacts systems where PostgreSQL is used or administered; relevant for developers/operations.
	- Score: 10
- Title: New Chrome Vulnerability Enables Cross-Origin Data Leak via Loader Referrer Policy
	- Reason: Affects Google Chrome, a primary browser for web app testing and use. Cross-origin data leaks can have direct impact on web app security.
	- Score: 9
- Title: New Chrome Zero-Day Actively Exploited; Google Issues Emergency Out-of-Band Patch
	- Reason: New Chrome V8 engine zero-day actively exploited. Highly relevant as V8 powers JavaScript execution—the backbone of web (and some hybrid mobile) apps.
	- Score: 10

## False positives:
- Title: Commvault Confirms Hackers Exploited CVE-2025-3928 as Zero-Day in Azure Breach
	- Reason: Newly discovered zero-day exploited in Azure environments via Commvault. Relevant for developers/ops deploying databases, backups, or workloads in Azure or using Commvault in cloud workflows.
	- Score: 8
- Title: Microsoft OneDrive File Picker Flaw Grants Apps Full Cloud Access — Even When Uploading Just One File
	- Reason: Web app developers using OneDrive integrations with JavaScript or Python in cloud apps are at risk until patched. New vulnerability with direct relevance for integrated workflows/devs.
	- Score: 8

## False negatives:
No results.



## Result 3
- Total relevant articles: 6
- Total articles found by AI agent: 7
- Total relevant articles found: 5
- Total false positives: 2
- Total false negatives: 1
- Recall: 0.83
- Precision: 0.71
- Time delta: 43.25s

## Articles found by AI agent:
- Qualcomm Fixes 3 Zero-Days Used in Targeted Android Attacks via Adreno GPU
- New Linux Flaws Allow Password Hash Theft via Core Dumps in Ubuntu, RHEL, Fedora
- New Chrome Zero-Day Actively Exploited; Google Issues Emergency Out-of-Band Patch
- New Chrome Vulnerability Enables Cross-Origin Data Leak via Loader Referrer Policy
- PostgreSQL Vulnerability Exploited Alongside BeyondTrust Zero-Day in Targeted Attacks
- Samsung Patches CVE-2025-4632 Used to Deploy Mirai Botnet via MagicINFO 9 Exploit
- Google Reports 75 Zero-Days Exploited in 2024 — 44% Targeted Enterprise Security Products

## Correctly classified articles:
- Title: New Linux Flaws Allow Password Hash Theft via Core Dumps in Ubuntu, RHEL, Fedora
	- Reason: This article details two newly discovered vulnerabilities (CVE-2025-5054 & CVE-2025-4598) affecting the core dump handling on major Linux distributions (Ubuntu, RHEL, Fedora). As a developer who deploys using Docker containers based on Linux images, these flaws could potentially expose sensitive credentials inside containers on affected bases.
	- Score: 8
- Title: Qualcomm Fixes 3 Zero-Days Used in Targeted Android Attacks via Adreno GPU
	- Reason: This article describes three newly discovered and patched zero-day vulnerabilities in Qualcomm's Adreno GPU, directly affecting the Android platform. Since you develop Android mobile applications, such kernel or hardware-related vulnerabilities can have major security implications for your user base, especially if you use devices with Qualcomm chipsets.
	- Score: 9
- Title: PostgreSQL Vulnerability Exploited Alongside BeyondTrust Zero-Day in Targeted Attacks
	- Reason: Describes a previously unknown SQL injection flaw (CVE-2025-1094) affecting the popular psql interactive tool in PostgreSQL. Since you use PostgreSQL as one of your major databases, this is directly relevant for understanding current and future risks in your stack.
	- Score: 9
- Title: New Chrome Vulnerability Enables Cross-Origin Data Leak via Loader Referrer Policy
	- Reason: Highlights a newly disclosed Chrome vulnerability affecting the referrer policy enforcement in the Loader component. As a web developer targeting browsers, such cross-origin leaks are relevant for both application security and user data privacy.
	- Score: 8
- Title: New Chrome Zero-Day Actively Exploited; Google Issues Emergency Out-of-Band Patch
	- Reason: Describes an actively exploited new Chrome vulnerability (CVE-2025-5419) in the V8 JavaScript/WebAssembly engine with a high CVSS score. Since you develop JavaScript-based web applications, browser zero-days in widely used engines directly relate to both your development work and to your users’ security.
	- Score: 10

## False positives:
- Title: Google Reports 75 Zero-Days Exploited in 2024 — 44% Targeted Enterprise Security Products
	- Reason: This report provides an overview of zero-days found in 2024, with a focus on browsers and mobile devices. Since you work with both web and mobile apps, trends in zero-days for platforms you target are very relevant for your threat model.
	- Score: 8
- Title: Samsung Patches CVE-2025-4632 Used to Deploy Mirai Botnet via MagicINFO 9 Exploit
	- Reason: Details a new critical path traversal vulnerability in Samsung MagicINFO 9 Server, used in targeted attacks. Since Samsung is one of your target mobile hardware vendors, newly discovered critical vulnerabilities in their ecosystem are highly relevant for mobile app security awareness.
	- Score: 8

## False negatives:
- Title: Microsoft Fixes 78 Flaws, 5 Zero-Days Exploited; CVSS 10 Bug Impacts Azure DevOps Server
	- Reason: Lists a batch of new vulnerabilities in Microsoft products including an Azure DevOps CVSS 10 flaw. If you ever interact with DevOps pipelines or integrate with Azure services, such flaws can be of indirect relevance.
	- Score: 6
