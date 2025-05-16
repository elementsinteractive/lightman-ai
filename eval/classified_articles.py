from hackerman_ai.article.models import Article

NON_RELEVANT_ARTICLES = {
    Article(
        link="https://thehackernews.com/2025/05/tiktok-slammed-with-530-million-gdpr.html",
        title="TikTok Slammed With €530 Million GDPR Fine for Sending E.U. Data to China",
        description='Ireland\'s Data Protection Commission (DPC) on Friday fined popular video-sharing platform TikTok €530 million ($601 million) for infringing data protection regulations in the region by transferring European users\' data to China.\n"TikTok infringed the GDPR regarding its transfers of EEA [European Economic Area] User Data to China and its transparency requirements," the DPC said in a statement. "',
    ),
    Article(
        link="https://thehackernews.com/2025/05/how-to-automate-cve-and-vulnerability.html",
        title="How to Automate CVE and Vulnerability Advisory Response with Tines",
        description="Run by the team at workflow orchestration and AI platform Tines, the Tines library features pre-built workflows shared by security practitioners from across the community - all free to import and deploy through the platform’s Community Edition.\nA recent standout is a workflow that automates monitoring for security advisories from CISA and other vendors, enriches advisories with CrowdStrike",
    ),
    Article(
        link="https://thehackernews.com/2025/05/mintsloader-drops-ghostweaver-via.html",
        title="MintsLoader Drops GhostWeaver via Phishing, ClickFix — Uses DGA, TLS for Stealth Attacks",
        description='The malware loader known as MintsLoader has been used to deliver a PowerShell-based remote access trojan called GhostWeaver.\n"MintsLoader operates through a multi-stage infection chain involving obfuscated JavaScript and PowerShell scripts," Recorded Future\'s Insikt Group said in a report shared with The Hacker News.\n"The malware employs sandbox and virtual machine evasion techniques, a domain',
    ),
    Article(
        link="https://thehackernews.com/2025/05/microsoft-sets-passkeys-default-for-new.html",
        title="Microsoft Sets Passkeys Default for New Accounts; 15 Billion Users Gain Passwordless Support",
        description="A year after Microsoft announced passkeys support for consumer accounts, the tech giant has announced a big change that pushes individuals signing up for new accounts to use the phishing-resistant authentication method by default.\n\"Brand new Microsoft accounts will now be 'passwordless by default,'\" Microsoft's Joy Chik and Vasu Jakkal said. \"New users will have several passwordless options for",
    ),
    Article(
        link="https://thehackernews.com/2025/05/why-top-soc-teams-are-shifting-to.html",
        title="Why top SOC teams are shifting to Network Detection and Response",
        description="Security Operations Center (SOC) teams are facing a fundamentally new challenge &mdash; traditional cybersecurity tools are failing to detect advanced adversaries who have become experts at evading endpoint-based defenses and signature-based detection systems. The reality of these &ldquo;invisible intruders&rdquo; is driving a significant need for a multi-layered approach to detecting threats,",
    ),
    Article(
        link="https://thehackernews.com/2025/05/claude-ai-exploited-to-operate-100-fake.html",
        title="Claude AI Exploited to Operate 100+ Fake Political Personas in Global Influence Campaign",
        description='Artificial intelligence (AI) company Anthropic has revealed that unknown threat actors leveraged its Claude chatbot for an "influence-as-a-service" operation to engage with authentic accounts across Facebook and X.\nThe sophisticated activity, branded as financially-motivated, is said to have used its AI tool to orchestrate 100 distinct personas on the two social media platforms, creating a',
    ),
    Article(
        link="https://thehackernews.com/2025/05/new-research-reveals-95-of-appsec-fixes.html",
        title="New Research Reveals: 95% of AppSec Fixes Don’t Reduce Risk",
        description="For over a decade, application security teams have faced a brutal irony: the more advanced the detection tools became, the less useful their results proved to be. As alerts from static analysis tools, scanners, and CVE databases surged, the promise of better security grew more distant. In its place, a new reality took hold—one defined by alert fatigue and overwhelmed teams.\nAccording to OX",
    ),
    Article(
        link="https://thehackernews.com/2025/05/darkwatchman-sheriff-malware-hit-russia.html",
        title="DarkWatchman, Sheriff Malware Hit Russia and Ukraine with Stealth and Nation-Grade Tactics",
        description="Russian companies have been targeted as part of a large-scale phishing campaign that's designed to deliver a known malware called DarkWatchman.\nTargets of the attacks include entities in the media, tourism, finance and insurance, manufacturing, retail, energy, telecom, transport, and biotechnology sectors, Russian cybersecurity company F6 said.\nThe activity is assessed to be the work of a",
    ),
    Article(
        link="https://thehackernews.com/2025/05/sonicwall-confirms-active-exploitation.html",
        title="SonicWall Confirms Active Exploitation of Flaws Affecting Multiple Appliance Models",
        description="SonicWall has revealed that two now-patched security flaws impacting its SMA100 Secure Mobile Access (SMA) appliances have been exploited in the wild.\nThe vulnerabilities in question are listed below -\n\nCVE-2023-44221 (CVSS score: 7.2) - Improper neutralization of special group in the SMA100 SSL-VPN management interface allows a remote authenticated attacker with administrative privilege to",
    ),
    Article(
        link="https://thehackernews.com/2025/04/experts-uncover-critical-mcp-and-a2a.html",
        title="Researchers Demonstrate How MCP Prompt Injection Can Be Used for Both Attack and Defense",
        description="As the field of artificial intelligence (AI) continues to evolve at a rapid pace, fresh research has found how techniques that render the Model Context Protocol (MCP) susceptible to prompt injection attacks could be used to develop security tooling or identify malicious tools, according to a new report from Tenable.\nMCP, launched by Anthropic in November 2024, is a framework designed to connect",
    ),
    Article(
        link="https://thehackernews.com/2025/04/free-webinar-guide-to-securing-your.html",
        title="[Free Webinar] Guide to Securing Your Entire Identity Lifecycle Against AI-Powered Threats",
        description="How Many Gaps Are Hiding in Your Identity System? It’s not just about logins anymore.\nToday’s attackers don’t need to “hack” in—they can trick their way in. Deepfakes, impersonation scams, and AI-powered social engineering are helping them bypass traditional defenses and slip through unnoticed. Once inside, they can take over accounts, move laterally, and cause long-term damage—all without",
    ),
    Article(
        link="https://thehackernews.com/2025/04/chinese-hackers-abuse-ipv6-slaac-for.html",
        title="Chinese Hackers Abuse IPv6 SLAAC for AitM Attacks via Spellbinder Lateral Movement Tool",
        description='A China-aligned advanced persistent threat (APT) group called TheWizards has been linked to a lateral movement tool called Spellbinder that can facilitate adversary-in-the-middle (AitM) attacks.\n"Spellbinder enables adversary-in-the-middle (AitM) attacks, through IPv6 stateless address autoconfiguration (SLAAC) spoofing, to move laterally in the compromised network, intercepting packets and',
    ),
    Article(
        link="https://thehackernews.com/2025/04/customer-account-takeovers-multi.html",
        title="Customer Account Takeovers: The Multi-Billion Dollar Problem You Don’t Know About",
        description="Everyone has cybersecurity stories involving family members. Here’s a relatively common one. The conversation usually goes something like this:&nbsp;\n“The strangest thing happened to my streaming account. I got locked out of my account, so I had to change my password. When I logged back in, all my shows were gone. Everything was in Spanish and there were all these Spanish shows I’ve never seen",
    ),
    Article(
        link="https://thehackernews.com/2025/04/nebulous-mantis-targets-nato-linked.html",
        title="Nebulous Mantis Targets NATO-Linked Entities with Multi-Stage Malware Attacks",
        description='Cybersecurity researchers have shed light on a Russian-speaking cyber espionage group called Nebulous Mantis that has deployed a remote access trojan called RomCom RAT since mid-2022.\nRomCom "employs advanced evasion techniques, including living-off-the-land (LOTL) tactics and encrypted command and control (C2) communications, while continuously evolving its infrastructure – leveraging',
    ),
    Article(
        link="https://thehackernews.com/2025/04/ransomhub-went-dark-april-1-affiliates.html",
        title="RansomHub Went Dark April 1; Affiliates Fled to Qilin, DragonForce Claimed Control",
        description='Cybersecurity researchers have revealed that RansomHub\'s online infrastructure has "inexplicably" gone offline as of April 1, 2025, prompting concerns among affiliates of the ransomware-as-a-service (RaaS) operation.\nSingaporean cybersecurity company Group-IB said that this may have caused affiliates to migrate to Qilin, given that "disclosures on its DLS [data leak site] have doubled since',
    ),
    Article(
        link="https://thehackernews.com/2025/04/meta-launches-llamafirewall-framework.html",
        title="Meta Launches LlamaFirewall Framework to Stop AI Jailbreaks, Injections, and Insecure Code",
        description="Meta on Tuesday announced LlamaFirewall, an open-source framework designed to secure artificial intelligence (AI) systems against emerging cyber risks such as prompt injection, jailbreaks, and insecure code, among others.\nThe framework, the company said, incorporates three guardrails, including PromptGuard 2, Agent Alignment Checks, and CodeShield.\nPromptGuard 2 is designed to detect direct",
    ),
    Article(
        link="https://thehackernews.com/2025/04/indian-court-orders-action-to-block.html",
        title="Indian Court Orders Action to Block Proton Mail Over AI Deepfake Abuse Allegations",
        description="A high court in the Indian state of Karnataka has ordered the blocking of end-to-end encrypted email provider Proton Mail across the country.\nThe High Court of Karnataka, on April 29, said the ruling was in response to a legal complaint filed by M Moser Design Associated India Pvt Ltd in January 2025.\n\nThe complaint alleged its staff had received e-mails containing obscene, abusive",
    ),
    Article(
        link="https://thehackernews.com/2025/04/whatsapp-launches-private-processing-to.html",
        title="WhatsApp Launches Private Processing to Enable AI Features While Protecting Message Privacy",
        description='Popular messaging app WhatsApp on Tuesday unveiled a new technology called Private Processing to enable artificial intelligence (AI) capabilities in a privacy-preserving manner.\n"Private Processing will allow users to leverage powerful optional AI features – like summarizing unread messages or editing help – while preserving WhatsApp\'s core privacy promise," the Meta-owned service said in a',
    ),
    Article(
        link="https://thehackernews.com/2025/04/new-reports-uncover-jailbreaks-unsafe.html",
        title="New Reports Uncover Jailbreaks, Unsafe Code, and Data Theft Risks in Leading AI Systems",
        description="Various generative artificial intelligence (GenAI) services have been found vulnerable to two types of jailbreak attacks that make it possible to produce illicit or dangerous content.\nThe first of the two techniques, codenamed Inception, instructs an AI tool to imagine a fictitious scenario, which can then be adapted into a second scenario within the first one where there exists no safety",
    ),
    Article(
        link="https://thehackernews.com/2025/04/sentinelone-uncovers-chinese-espionage.html",
        title="SentinelOne Uncovers Chinese Espionage Campaign Targeting Its Infrastructure and Clients",
        description='Cybersecurity company SentinelOne has revealed that a China-nexus threat cluster dubbed PurpleHaze conducted reconnaissance attempts against its infrastructure and some of its high-value customers.\n"We first became aware of this threat cluster during a 2024 intrusion conducted against an organization previously providing hardware logistics services for SentinelOne employees," security',
    ),
    Article(
        link="https://thehackernews.com/2025/04/product-walkthrough-securing-microsoft.html",
        title="Product Walkthrough: Securing Microsoft Copilot with Reco",
        description="Find out how Reco keeps Microsoft 365 Copilot safe by spotting risky prompts, protecting data, managing user access, and identifying threats - all while keeping productivity high.\n\nMicrosoft 365 Copilot promises to boost productivity by turning natural language prompts into actions. Employees can generate reports, comb through data, or get instant answers just by asking Copilot.&nbsp;\nHowever,",
    ),
    Article(
        link="https://thehackernews.com/2025/04/google-reports-75-zero-days-exploited.html",
        title="Google Reports 75 Zero-Days Exploited in 2024 — 44% Targeted Enterprise Security Products",
        description='Google has revealed that it observed 75 zero-day vulnerabilities exploited in the wild in 2024, down from 98 in 2023 but an increase from 63 the year before.\nOf the 75 zero-days, 44% of them targeted enterprise products. As many as 20 flaws were identified in security software and appliances.\n"Zero-day exploitation of browsers and mobile devices fell drastically, decreasing by about a third for',
    ),
    Article(
        link="https://thehackernews.com/2025/04/malware-attack-targets-world-uyghur.html",
        title="Malware Attack Targets World Uyghur Congress Leaders via Trojanized UyghurEdit++ Tool",
        description="In a new campaign detected in March 2025, senior members of the World Uyghur Congress (WUC) living in exile have been targeted by a Windows-based malware that's capable of conducting surveillance.\nThe spear-phishing campaign involved the use of a trojanized version of a legitimate open-source word processing and spell check tool called UyghurEdit++ developed to support the use of the Uyghur",
    ),
    Article(
        link="https://thehackernews.com/2025/04/cisa-adds-actively-exploited-broadcom.html",
        title="CISA Adds Actively Exploited Broadcom and Commvault Flaws to KEV Database",
        description="The U.S. Cybersecurity and Infrastructure Security Agency (CISA) on Monday added two high-severity security flaws impacting Broadcom Brocade Fabric OS and Commvault Web Server to its Known Exploited Vulnerabilities (KEV) catalog, citing evidence of active exploitation in the wild.\nThe vulnerabilities in question are listed below -\n\nCVE-2025-1976 (CVSS score: 8.6) - A code injection flaw",
    ),
    Article(
        link="https://thehackernews.com/2025/04/weekly-recap-critical-sap-exploit-ai.html",
        title="⚡ Weekly Recap: Critical SAP Exploit, AI-Powered Phishing, Major Breaches, New CVEs & More",
        description="What happens when cybercriminals no longer need deep skills to breach your defenses? Today’s attackers are armed with powerful tools that do the heavy lifting — from AI-powered phishing kits to large botnets ready to strike. And they’re not just after big corporations. Anyone can be a target when fake identities, hijacked infrastructure, and insider tricks are used to slip past security",
    ),
    Article(
        link="https://thehackernews.com/2025/04/how-breaches-start-breaking-down-5-real.html",
        title="How Breaches Start: Breaking Down 5 Real Vulns",
        description="Not every security vulnerability is high risk on its own - but in the hands of an advanced attacker, even small weaknesses can escalate into major breaches. These five real vulnerabilities, uncovered by Intruder’s bug-hunting team, reveal how attackers turn overlooked flaws into serious security incidents.\n1. Stealing AWS Credentials with a Redirect\n\nServer-Side Request Forgery (SSRF) is a",
    ),
    Article(
        link="https://thehackernews.com/2025/04/earth-kurma-targets-southeast-asia-with.html",
        title="Earth Kurma Targets Southeast Asia With Rootkits and Cloud-Based Data Theft Tools",
        description='Government and telecommunications sectors in Southeast Asia have become the target of a "sophisticated" campaign undertaken by a new advanced persistent threat (APT) group called Earth Kurma since June 2024.\nThe attacks, per Trend Micro, have leveraged custom malware, rootkits, and cloud storage services for data exfiltration. The Philippines, Vietnam, Thailand, and Malaysia are among the',
    ),
    Article(
        link="https://thehackernews.com/2025/04/woocommerce-users-targeted-by-fake.html",
        title="WooCommerce Users Targeted by Fake Patch Phishing Campaign Deploying Site Backdoors",
        description='Cybersecurity researchers are warning about a large-scale phishing campaign targeting WooCommerce users with a fake security alert urging them to download a "critical patch" but deploy a backdoor instead.\nWordPress security company Patchstack described the activity as sophisticated and a variant of another campaign observed in December 2023 that employed a fake CVE ploy to breach sites running',
    ),
    Article(
        link="https://thehackernews.com/2025/04/storm-1977-hits-education-clouds-with.html",
        title="Storm-1977 Hits Education Clouds with AzureChecker, Deploys 200+ Crypto Mining Containers",
        description='Microsoft has revealed that a threat actor it tracks as Storm-1977 has conducted password spraying attacks against cloud tenants in the education sector over the past year.\n"The attack involves the use of AzureChecker.exe, a Command Line Interface (CLI) tool that is being used by a wide range of threat actors," the Microsoft Threat Intelligence team said in an analysis.\nThe tech giant noted that',
    ),
    Article(
        link="https://thehackernews.com/2025/04/toymaker-uses-lagtoy-to-sell-access-to.html",
        title="ToyMaker Uses LAGTOY to Sell Access to CACTUS Ransomware Gangs for Double Extortion",
        description='Cybersecurity researchers have detailed the activities of an initial access broker (IAB) dubbed ToyMaker that has been observed handing over access to double extortion ransomware gangs like CACTUS.\nThe IAB has been assessed with medium confidence to be a financially motivated threat actor, scanning for vulnerable systems and deploying a custom malware called LAGTOY (aka HOLERUN).\n"LAGTOY can be',
    ),
    Article(
        link="https://thehackernews.com/2025/04/north-korean-hackers-spread-malware-via.html",
        title="North Korean Hackers Spread Malware via Fake Crypto Firms and Job Interview Lures",
        description='North Korea-linked threat actors behind the Contagious Interview have set up front companies as a way to distribute malware during the fake hiring process.\n"In this new campaign, the threat actor group is using three front companies in the cryptocurrency consulting industry – BlockNovas LLC (blocknovas[.] com  ), Angeloper Agency (angeloper[.]com ,and SoftGlide LLC (softglide[.]co) – to spread',
    ),
    Article(
        link="https://thehackernews.com/2025/04/sap-confirms-critical-netweaver-flaw.html",
        title="New Critical SAP NetWeaver Flaw Exploited to Drop Web Shell, Brute Ratel Framework",
        description='Threat actors are likely exploiting a new vulnerability in SAP NetWeaver to upload JSP web shells with the goal of facilitating unauthorized file uploads and code execution.&nbsp;\n"The exploitation is likely tied to either a previously disclosed vulnerability like CVE-2017-9844 or an unreported remote file inclusion (RFI) issue," ReliaQuest said in a report published this week.\nThe cybersecurity',
    ),
    Article(
        link="https://thehackernews.com/2025/04/why-nhis-are-securitys-most-dangerous.html",
        title="Why NHIs Are Security's Most Dangerous Blind Spot",
        description="When we talk about identity in cybersecurity, most people think of usernames, passwords, and the occasional MFA prompt. But lurking beneath the surface is a growing threat that does not involve human credentials at all, as we witness the exponential growth of Non-Human Identities (NHIs).&nbsp;\nAt the top of mind when NHIs are mentioned, most security teams immediately think of Service Accounts.",
    ),
    Article(
        link="https://thehackernews.com/2025/04/researchers-identify-rackstatic.html",
        title="Researchers Identify Rack::Static Vulnerability Enabling Data Breaches in Ruby Servers",
        description="Cybersecurity researchers have disclosed three security flaws in the Rack Ruby web server interface that, if successfully exploited, could enable attackers to gain unauthorized access to files, inject malicious data, and tamper with logs under certain conditions.\nThe vulnerabilities, flagged by cybersecurity vendor OPSWAT, are listed below -\n\nCVE-2025-27610 (CVSS score: 7.5) - A path traversal",
    ),
    Article(
        link="https://thehackernews.com/2025/04/dslogdrat-malware-deployed-via-ivanti.html",
        title="DslogdRAT Malware Deployed via Ivanti ICS Zero-Day CVE-2025-0282 in Japan Attacks",
        description='Cybersecurity researchers are warning about a new malware called DslogdRAT that\'s installed following the exploitation of a now-patched security flaw in Ivanti Connect Secure (ICS).\nThe malware, along with a web shell, were "installed by exploiting a zero-day vulnerability at that time, CVE-2025-0282, during attacks against organizations in Japan around December 2024," JPCERT/CC researcher Yuma',
    ),
    Article(
        link="https://thehackernews.com/2025/04/lazarus-hits-6-south-korean-firms-via.html",
        title="Lazarus Hits 6 South Korean Firms via Cross EX, Innorix Flaws and ThreatNeedle Malware",
        description="At least six organizations in South Korea have been targeted by the prolific North Korea-linked Lazarus Group as part of a campaign dubbed Operation SyncHole.\nThe activity targeted South Korea's software, IT, financial, semiconductor manufacturing, and telecommunications industries, according to a report from Kaspersky published today. The earliest evidence of compromise was first detected in",
    ),
    Article(
        link="https://thehackernews.com/2025/04/linux-iouring-poc-rootkit-bypasses.html",
        title="Linux io_uring PoC Rootkit Bypasses System Call-Based Threat Detection Tools",
        description='Cybersecurity researchers have demonstrated a proof-of-concept (PoC) rootkit dubbed Curing that leverages a Linux asynchronous I/O mechanism called io_uring to bypass traditional system call monitoring.\nThis causes a "major blind spot in Linux runtime security tools," ARMO said.\n"This mechanism allows a user application to perform various actions without using system calls," the company said in',
    ),
    Article(
        link="https://thehackernews.com/2025/04/automating-zero-trust-in-healthcare.html",
        title="Automating Zero Trust in Healthcare: From Risk Scoring to Dynamic Policy Enforcement Without Network Redesign",
        description="The Evolving Healthcare Cybersecurity Landscape&nbsp;\nHealthcare organizations face unprecedented cybersecurity challenges in 2025. With operational technology (OT) environments increasingly targeted and the convergence of IT and medical systems creating an expanded attack surface, traditional security approaches are proving inadequate. According to recent statistics, the healthcare sector",
    ),
    Article(
        link="https://thehackernews.com/2025/04/159-cves-exploited-in-q1-2025-283.html",
        title="159 CVEs Exploited in Q1 2025 — 28.3% Within 24 Hours of Disclosure",
        description='As many as 159 CVE identifiers have been flagged as exploited in the wild in the first quarter of 2025, up from 151 in Q4 2024.\n"We continue to see vulnerabilities being exploited at a fast pace with 28.3% of vulnerabilities being exploited within 1-day of their CVE disclosure," VulnCheck said in a report shared with The Hacker News.\nThis translates to 45 security flaws that have been weaponized',
    ),
    Article(
        link="https://thehackernews.com/2025/04/darcula-adds-genai-to-phishing-toolkit.html",
        title="Darcula Adds GenAI to Phishing Toolkit, Lowering the Barrier for Cybercriminals",
        description='The threat actors behind the Darcula phishing-as-a-service (PhaaS) platform have released new updates to their cybercrime suite with generative artificial intelligence (GenAI) capabilities.\n"This addition lowers the technical barrier for creating phishing pages, enabling less tech-savvy criminals to deploy customized scams in minutes," Netcraft said in a fresh report shared with The Hacker News.',
    ),
    Article(
        link="https://thehackernews.com/2025/04/whatsapp-adds-advanced-chat-privacy-to.html",
        title="WhatsApp Adds Advanced Chat Privacy to Blocks Chat Exports and Auto-Downloads",
        description='WhatsApp has introduced an extra layer of privacy called Advanced Chat Privacy that allows users to block participants from sharing the contents of a conversation in traditional chats and groups.\n"This new setting available in both chats and groups helps prevent others from taking content outside of WhatsApp for when you may want extra privacy," WhatsApp said in a statement.\nThe optional feature',
    ),
    Article(
        link="https://thehackernews.com/2025/04/dprk-hackers-steal-137m-from-tron-users.html",
        title="DPRK Hackers Steal $137M from TRON Users in Single-Day Phishing Attack",
        description='Multiple threat activity clusters with ties to North Korea (aka Democratic People\'s Republic of Korea or DPRK) have been linked to attacks targeting organizations and individuals in the Web3 and cryptocurrency space.\n"The focus on Web3 and cryptocurrency appears to be primarily financially motivated due to the heavy sanctions that have been placed on North Korea," Google-owned Mandiant said in',
    ),
    Article(
        link="https://thehackernews.com/2025/04/iran-linked-hackers-target-israel-with.html",
        title="Iran-Linked Hackers Target Israel with MURKYTOUR Malware via Fake Job Campaign",
        description='The Iran-nexus threat actor known as UNC2428 has been observed delivering a backdoor known as MURKYTOUR as part of a job-themed social engineering campaign aimed at Israel in October 2024.\nGoogle-owned Mandiant described UNC2428 as a threat actor aligned with Iran that engages in cyber espionage-related operations. The intrusion set is said to have distributed the malware through a "complex',
    ),
    Article(
        link="https://thehackernews.com/2025/04/android-spyware-disguised-as-alpine.html",
        title="Android Spyware Disguised as Alpine Quest App Targets Russian Military Devices",
        description='Cybersecurity researchers have revealed that Russian military personnel are the target of a new malicious campaign that distributes Android spyware under the guise of the Alpine Quest mapping software.\n"The attackers hide this trojan inside modified Alpine Quest mapping software and distribute it in various ways, including through one of the Russian Android app catalogs," Doctor Web said in an',
    ),
    Article(
        link="https://thehackernews.com/2025/04/three-reasons-why-browser-is-best-for.html",
        title="Three Reasons Why the Browser is Best for Stopping Phishing Attacks",
        description="Phishing attacks remain a huge challenge for organizations in 2025. In fact, with attackers increasingly leveraging identity-based techniques over software exploits, phishing arguably poses a bigger threat than ever before.&nbsp;\nAttackers are increasingly leveraging identity-based techniques over software exploits, with phishing and stolen credentials (a byproduct of phishing) now the primary",
    ),
    Article(
        link="https://thehackernews.com/2025/04/russian-hackers-exploit-microsoft-oauth.html",
        title="Russian Hackers Exploit Microsoft OAuth to Target Ukraine Allies via Signal and WhatsApp",
        description='Multiple suspected Russia-linked threat actors are "aggressively" targeting individuals and organizations with ties to Ukraine and human rights with an aim to gain unauthorized access to Microsoft 365 accounts since early March 2025.\nThe highly targeted social engineering operations, per Volexity, are a shift from previously documented attacks that leveraged a technique known as device code',
    ),
    Article(
        link="https://thehackernews.com/2025/05/coinbase-agents-bribed-data-of-1-users.html",
        title="Coinbase Agents Bribed, Data of ~1% Users Leaked; $20M Extortion Attempt Fails",
        description='Cryptocurrency exchange Coinbase has disclosed that unknown cyber actors broke into its systems and stole account data for a small subset of its customers.\n"Criminals targeted our customer support agents overseas," the company said in a statement. "They used cash offers to convince a small group of insiders to copy data in our customer support tools for less than 1% of Coinbase monthly',
    ),
    Article(
        link="https://thehackernews.com/2025/05/pen-testing-for-compliance-only-its.html",
        title="Pen Testing for Compliance Only? It's Time to Change Your Approach",
        description="Imagine this: Your organization completed its annual penetration test in January, earning high marks for security compliance. In February, your development team deployed a routine software update. By April, attackers had already exploited a vulnerability introduced in that February update, gaining access to customer data weeks before being finally detected.\nThis situation isn't theoretical: it",
    ),
    Article(
        link="https://thehackernews.com/2025/05/top-5-bcdr-capabilities-for-ransomware-defense.html",
        title="5 BCDR Essentials for Effective Ransomware Defense",
        description="Ransomware has evolved into a deceptive, highly coordinated and dangerously sophisticated threat capable of crippling organizations of any size. Cybercriminals now exploit even legitimate IT tools to infiltrate networks and launch ransomware attacks. In a chilling example, Microsoft recently disclosed how threat actors misused its Quick Assist remote assistance tool to deploy the destructive",
    ),
    Article(
        link="https://thehackernews.com/2025/05/russia-linked-apt28-exploited-mdaemon.html",
        title="Russia-Linked APT28 Exploited MDaemon Zero-Day to Hack Government Webmail Servers",
        description="A Russia-linked threat actor has been attributed to a cyber espionage operation targeting webmail servers such as Roundcube, Horde, MDaemon, and Zimbra via cross-site scripting (XSS) vulnerabilities, including a then-zero-day in MDaemon, according to new findings from ESET.\nThe activity, which commenced in 2023, has been codenamed Operation RoundPress by the Slovak cybersecurity company. It has",
    ),
    Article(
        link="https://thehackernews.com/2025/05/malicious-npm-package-leverages-unicode.html",
        title="Malicious npm Package Leverages Unicode Steganography, Google Calendar as C2 Dropper",
        description='Cybersecurity researchers have discovered a malicious package named "os-info-checker-es6" that disguises itself as an operating system information utility to stealthily drop a next-stage payload onto compromised systems.\n"This campaign employs clever Unicode-based steganography to hide its initial malicious code and utilizes a Google Calendar event short link as a dynamic dropper for its final',
    ),
    Article(
        link="https://thehackernews.com/2025/05/samsung-patches-cve-2025-4632-used-to.html",
        title="Samsung Patches CVE-2025-4632 Used to Deploy Mirai Botnet via MagicINFO 9 Exploit",
        description='Samsung has released software updates to address a critical security flaw in MagicINFO 9 Server that has been actively exploited in the wild.\nThe vulnerability, tracked as CVE-2025-4632 (CVSS score: 9.8), has been described as a path traversal flaw.\n"Improper limitation of a pathname to a restricted directory vulnerability in Samsung MagicINFO 9 Server version before 21.1052 allows attackers to',
    ),
    Article(
        link="https://thehackernews.com/2025/05/bianlian-and-ransomexx-exploit-sap.html",
        title="BianLian and RansomExx Exploit SAP NetWeaver Flaw to Deploy PipeMagic Trojan",
        description="At least two different cybercrime groups BianLian and RansomExx are said to have exploited a recently disclosed security flaw in SAP NetWeaver tracked as CVE-2025-31324, indicating that multiple threat actors are taking advantage of the bug.\nCybersecurity firm ReliaQuest, in a new update published today, said it uncovered evidence suggesting involvement from the BianLian data extortion crew and",
    ),
    Article(
        link="https://thehackernews.com/2025/05/xinbi-telegram-market-tied-to-84b-in.html",
        title="Xinbi Telegram Market Tied to $8.4B in Crypto Crime, Romance Scams, North Korea Laundering",
        description="A Chinese-language, Telegram-based marketplace called Xinbi Guarantee has facilitated no less than $8.4 billion in transactions since 2022, making it the second major black market to be exposed after HuiOne Guarantee.\nAccording to a report published by blockchain analytics firm Elliptic, merchants on the marketplace have been found to peddle technology, personal data, and money laundering",
    ),
    Article(
        link="https://thehackernews.com/2025/05/ctm360-identifies-surge-in-phishing.html",
        title="CTM360 Identifies Surge in Phishing Attacks Targeting Meta Business Users",
        description='A new global phishing threat called "Meta Mirage" has been uncovered, targeting businesses using Meta\'s Business Suite. This campaign specifically aims at hijacking high-value accounts, including those managing advertising and official brand pages.\nCybersecurity researchers at CTM360 revealed that attackers behind Meta Mirage impersonate official Meta communications, tricking users into handing',
    ),
    Article(
        link="https://thehackernews.com/2025/05/earth-ammit-breached-drone-supply.html",
        title="Earth Ammit Breached Drone Supply Chains via ERP in VENOM, TIDRONE Campaigns",
        description="A cyber espionage group known as Earth Ammit has been linked to two related but distinct campaigns from 2023 to 2024 targeting various entities in Taiwan and South Korea, including military, satellite, heavy industry, media, technology, software services, and healthcare sectors.\nCybersecurity firm Trend Micro said the first wave, codenamed VENOM, mainly targeted software service providers, while",
    ),
    Article(
        link="https://thehackernews.com/2025/05/learning-how-to-hack-why-offensive.html",
        title="Learning How to Hack: Why Offensive Security Training Benefits Your Entire Security Team",
        description="Organizations across industries are experiencing significant escalations in cyberattacks, particularly targeting critical infrastructure providers and cloud-based enterprises. Verizon’s recently released 2025 Data Breach Investigations Report found an 18% YoY increase in confirmed breaches, with the exploitation of vulnerabilities as an initial access step growing by 34%.&nbsp;\nAs attacks rise",
    ),
    Article(
        link="https://thehackernews.com/2025/05/horabot-malware-targets-6-latin.html",
        title="Horabot Malware Targets 6 Latin American Nations Using Invoice-Themed Phishing Emails",
        description="Cybersecurity researchers have discovered a new phishing campaign that's being used to distribute malware called Horabot targeting Windows users in Latin American countries like Mexico, Guatemala, Colombia, Peru, Chile, and Argentina.\nThe campaign is \"using crafted emails that impersonate invoices or financial documents to trick victims into opening malicious attachments and can steal email",
    ),
    Article(
        link="https://thehackernews.com/2025/05/microsoft-fixes-78-flaws-5-zero-days.html",
        title="Microsoft Fixes 78 Flaws, 5 Zero-Days Exploited; CVSS 10 Bug Impacts Azure DevOps Server",
        description="Microsoft on Tuesday shipped fixes to address a total of 78 security flaws across its software lineup, including a set of five zero-days that have come under active exploitation in the wild.\nOf the 78 flaws resolved by the tech giant, 11 are rated Critical, 66 are rated Important, and one is rated Low in severity. Twenty-eight of these vulnerabilities lead to remote code execution, 21 of them",
    ),
    Article(
        link="https://thehackernews.com/2025/05/fortinet-patches-cve-2025-32756-zero.html",
        title="Fortinet Patches CVE-2025-32756 Zero-Day RCE Flaw Exploited in FortiVoice Systems",
        description='Fortinet has patched a critical security flaw that it said has been exploited as a zero-day in attacks targeting FortiVoice enterprise phone systems.\nThe vulnerability, tracked as CVE-2025-32756, carries a CVSS score of 9.6 out of 10.0.\n"A stack-based overflow vulnerability [CWE-121] in FortiVoice, FortiMail, FortiNDR, FortiRecorder, and FortiCamera may allow a remote unauthenticated attacker to',
    ),
    Article(
        link="https://thehackernews.com/2025/05/ivanti-patches-epmm-vulnerabilities.html",
        title="Ivanti Patches EPMM Vulnerabilities Exploited for Remote Code Execution in Limited Attacks",
        description="Ivanti has released security updates to address two security flaws in Endpoint Manager Mobile (EPMM) software that have been chained in attacks to gain remote code execution.\nThe vulnerabilities in question are listed below -\n\nCVE-2025-4427 (CVSS score: 5.3) - An authentication bypass in Ivanti Endpoint Manager Mobile allowing attackers to access protected resources without proper credentials",
    ),
    Article(
        link="https://thehackernews.com/2025/05/china-linked-apts-exploit-sap-cve-2025.html",
        title="China-Linked APTs Exploit SAP CVE-2025-31324 to Breach 581 Critical Systems Worldwide",
        description='A recently disclosed critical security flaw impacting SAP NetWeaver is being exploited by multiple China-nexus nation-state actors to target critical infrastructure networks.\n"Actors leveraged CVE-2025-31324, an unauthenticated file upload vulnerability that enables remote code execution (RCE)," EclecticIQ researcher Arda Büyükkaya said in an analysis published today.\nTargets of the campaign',
    ),
    Article(
        link="https://thehackernews.com/2025/05/malicious-pypi-package-posing-as-solana.html",
        title="Malicious PyPI Package Posing as Solana Tool Stole Source Code in 761 Downloads",
        description="Cybersecurity researchers have discovered a malicious package on the Python Package Index (PyPI) repository that purports to be an application related to the Solana blockchain, but contains malicious functionality to steal source code and developer secrets.\nThe package, named solana-token, is no longer available for download from PyPI, but not before it was downloaded 761 times. It was first",
    ),
    Article(
        link="https://thehackernews.com/2025/05/deepfake-defense-in-age-of-ai.html",
        title="Deepfake Defense in the Age of AI",
        description="The cybersecurity landscape has been dramatically reshaped by the advent of generative AI. Attackers now leverage large language models (LLMs) to impersonate trusted individuals and automate these social engineering tactics at scale.&nbsp;\nLet’s review the status of these rising attacks, what’s fueling them, and how to actually prevent, not detect, them.&nbsp;\nThe Most Powerful Person on the",
    ),
    Article(
        link="https://thehackernews.com/2025/05/north-korean-konni-apt-targets-ukraine.html",
        title="North Korean Konni APT Targets Ukraine with Malware to track Russian Invasion Progress",
        description='The North Korea-linked threat actor known as Konni APT has been attributed to a phishing campaign targeting government entities in Ukraine, indicating the threat actor\'s targeting beyond Russia.\nEnterprise security firm Proofpoint said the end goal of the campaign is to collect intelligence on the "trajectory of the Russian invasion."\n"The group\'s interest in Ukraine follows historical targeting',
    ),
    Article(
        link="https://thehackernews.com/2025/05/moldovan-police-arrest-suspect-in-45m.html",
        title="Moldovan Police Arrest Suspect in €4.5M Ransomware Attack on Dutch Research Agency",
        description='Moldovan law enforcement authorities have arrested a 45-year-old foreign man suspected of involvement in a series of ransomware attacks targeting Dutch companies in 2021.\n"He is wanted internationally for committing several cybercrimes (ransomware attacks, blackmail, and money laundering) against companies based in the Netherlands," officials said in a statement Monday.\nIn conjunction with the',
    ),
    Article(
        link="https://thehackernews.com/2025/05/turkiye-hackers-exploited-output.html",
        title="Türkiye Hackers Exploited Output Messenger Zero-Day to Drop Golang Backdoors on Kurdish Servers",
        description='A Türkiye-affiliated threat actor exploited a zero-day security flaw in an Indian enterprise communication platform called Output Messenger as part of a cyber espionage attack campaign since April 2024.\n"These exploits have resulted in a collection of related user data from targets in Iraq," the Microsoft Threat Intelligence team said. "The targets of the attack are associated with the Kurdish',
    ),
    Article(
        link="https://thehackernews.com/2025/05/asus-patches-driverhub-rce-flaws.html",
        title="ASUS Patches DriverHub RCE Flaws Exploitable via HTTP and Crafted .ini Files",
        description="ASUS has released updates to address two security flaws impacting ASUS DriverHub that, if successfully exploited, could enable an attacker to leverage the software in order to achieve remote code execution.\nDriverHub is a tool that's designed to automatically detect the motherboard model of a computer and display necessary driver updates for subsequent installation by communicating with a",
    ),
    Article(
        link="https://thehackernews.com/2025/05/weekly-recap-zero-day-exploits.html",
        title="⚡ Weekly Recap: Zero-Day Exploits, Developer Malware, IoT Botnets, and AI-Powered Scams",
        description="What do a source code editor, a smart billboard, and a web server have in common? They’ve all become launchpads for attacks—because cybercriminals are rethinking what counts as “infrastructure.” Instead of chasing high-value targets directly, threat actors are now quietly taking over the overlooked: outdated software, unpatched IoT devices, and open-source packages. It's not just clever—it’s",
    ),
    Article(
        link="https://thehackernews.com/2025/05/the-persistence-problem-why-exposed.html",
        title="The Persistence Problem: Why Exposed Credentials Remain Unfixed—and How to Change That",
        description="Detecting leaked credentials is only half the battle. The real challenge—and often the neglected half of the equation—is what happens after detection. New research from GitGuardian's State of Secrets Sprawl 2025 report reveals a disturbing trend: the vast majority of exposed company secrets discovered in public repositories remain valid for years after detection, creating an expanding attack",
    ),
    Article(
        link="https://thehackernews.com/2025/05/fake-ai-tools-used-to-spread.html",
        title="Fake AI Tools Used to Spread Noodlophile Malware, Targeting 62,000+ via Facebook Lures",
        description='Threat actors have been observed leveraging fake artificial intelligence (AI)-powered tools as a lure to entice users into downloading an information stealer malware dubbed Noodlophile.\n"Instead of relying on traditional phishing or cracked software sites, they build convincing AI-themed platforms – often advertised via legitimate-looking Facebook groups and viral social media campaigns,"',
    ),
    Article(
        link="https://thehackernews.com/2025/05/google-pays-1375-billion-to-texas-over.html",
        title="Google Pays $1.375 Billion to Texas Over Unauthorized Tracking and Biometric Data Collection",
        description="Google has agreed to pay the U.S. state of Texas nearly $1.4 billion to settle two lawsuits that accused the company of tracking users' personal location and maintaining their facial recognition data without consent.\nThe $1.375 billion payment dwarfs the fines the tech giant has paid to settle similar lawsuits brought by other U.S. states. In November 2022, it paid $391 million to a group of 40",
    ),
    Article(
        link="https://thehackernews.com/2025/05/germany-shuts-down-exch-over-19b.html",
        title="Germany Shuts Down eXch Over $1.9B Laundering, Seizes €34M in Crypto and 8TB of Data",
        description="Germany's Federal Criminal Police Office (aka Bundeskriminalamt or BKA) has seized the online infrastructure and shutdown linked to the eXch cryptocurrency exchange over allegations of money laundering and operating a criminal trading platform.\nThe operation was carried out on April 30, 2025, authorities said, adding they also confiscated 8 terabytes worth of data and cryptocurrency assets",
    ),
    Article(
        link="https://thehackernews.com/2025/05/breaking-7000-device-proxy-botnet-using.html",
        title="BREAKING: 7,000-Device Proxy Botnet Using IoT, EoL Systems Dismantled in U.S. - Dutch Operation",
        description="A joint law enforcement operation undertaken by Dutch and U.S. authorities has dismantled a criminal proxy network that's powered by thousands of infected Internet of Things (IoT) and end-of-life (EoL) devices, enlisting them into a botnet for providing anonymity to malicious actors.\nIn conjunction with the domain seizure, Russian nationals, Alexey Viktorovich Chertkov, 37, Kirill Vladimirovich",
    ),
    Article(
        link="https://thehackernews.com/2025/05/ottercookie-v4-adds-vm-detection-and.html",
        title="OtterCookie v4 Adds VM Detection and Chrome, MetaMask Credential Theft Capabilities",
        description='The North Korean threat actors behind the Contagious Interview campaign have been observed using updated versions of a cross-platform malware called OtterCookie with capabilities to steal credentials from web browsers and other files.\nNTT Security Holdings, which detailed the new findings, said the attackers have "actively and continuously" updated the malware, introducing versions v3 and v4 in',
    ),
    Article(
        link="https://thehackernews.com/2025/05/initial-access-brokers-target-brazil.html",
        title="Initial Access Brokers Target Brazil Execs via NF-e Spam and Legit RMM Trials",
        description='Cybersecurity researchers are warning of a new campaign that\'s targeting Portuguese-speaking users in Brazil with trial versions of commercial remote monitoring and management (RMM) software since January 2025.\n"The spam message uses the Brazilian electronic invoice system, NF-e, as a lure to entice users into clicking hyperlinks and accessing malicious content hosted in Dropbox," Cisco Talos',
    ),
    Article(
        link="https://thehackernews.com/2025/05/deploying-ai-agents-learn-to-secure.html",
        title="Deploying AI Agents? Learn to Secure Them Before Hackers Strike Your Business",
        description="AI agents are changing the way businesses work. They can answer questions, automate tasks, and create better user experiences. But with this power comes new risks — like data leaks, identity theft, and malicious misuse.\nIf your company is exploring or already using AI agents, you need to ask:&nbsp;Are they secure?\nAI agents work with sensitive data and make real-time decisions. If they’re not",
    ),
    Article(
        link="https://thehackernews.com/2025/05/beyond-vulnerability-management-cves.html",
        title="Beyond Vulnerability Management – Can You CVE What I CVE?",
        description="The Vulnerability Treadmill\nThe reactive nature of vulnerability management, combined with delays from policy and process, strains security teams. Capacity is limited and patching everything immediately is a struggle. Our Vulnerability Operation Center (VOC) dataset analysis identified 1,337,797 unique findings (security issues) across 68,500 unique customer assets. 32,585 of them were distinct",
    ),
    Article(
        link="https://thehackernews.com/2025/05/google-rolls-out-on-device-ai.html",
        title="Google Rolls Out On-Device AI Protections to Detect Scams in Chrome and Android",
        description="Google on Thursday announced it's rolling out new artificial intelligence (AI)-powered countermeasures to combat scams across Chrome, Search, and Android.\nThe tech giant said it will begin using Gemini Nano, its on-device large language model (LLM), to improve Safe Browsing in Chrome 137 on desktops.\n\"The on-device approach provides instant insight on risky websites and allows us to offer",
    ),
    Article(
        link="https://thehackernews.com/2025/05/chinese-hackers-exploit-sap-rce-flaw.html",
        title="Chinese Hackers Exploit SAP RCE Flaw CVE-2025-31324, Deploy Golang-Based SuperShell",
        description="A China-linked unnamed threat actor dubbed Chaya_004 has been observed exploiting a recently disclosed security flaw in SAP NetWeaver.\nForescout Vedere Labs, in a report published Thursday, said it uncovered a malicious infrastructure likely associated with the hacking group weaponizing CVE-2025-31324 (CVSS score: 10.0) since April 29, 2025.\nCVE-2025-31324 refers to a critical SAP NetWeaver flaw",
    ),
    Article(
        link="https://thehackernews.com/2025/05/38000-freedrain-subdomains-found.html",
        title="38,000+ FreeDrain Subdomains Found Exploiting SEO to Steal Crypto Wallet Seed Phrases",
        description='Cybersecurity researchers have exposed what they say is an "industrial-scale, global cryptocurrency phishing operation" engineered to steal digital assets from cryptocurrency wallets for several years.\nThe campaign has been codenamed FreeDrain by threat intelligence firms SentinelOne and Validin.\n"FreeDrain uses SEO manipulation, free-tier web services (like gitbook.io, webflow.io, and github.io',
    ),
    Article(
        link="https://thehackernews.com/2025/05/security-tools-alone-dont-protect-you.html",
        title="Security Tools Alone Don't Protect You — Control Effectiveness Does",
        description="61% of security leaders reported suffering a breach due to failed or misconfigured controls over the past 12 months. This is despite having an average of 43 cybersecurity tools in place.\nThis massive rate of security failure is clearly not a security investment problem. It is a configuration problem. Organizations are beginning to understand that a security control installed or deployed is not",
    ),
    Article(
        link="https://thehackernews.com/2025/05/sonicwall-patches-3-flaws-in-sma-100.html",
        title="SonicWall Patches 3 Flaws in SMA 100 Devices Allowing Attackers to Run Code as Root",
        description="SonicWall has released patches to address three security flaws affecting SMA 100 Secure Mobile Access (SMA) appliances that could be fashioned to result in remote code execution.\nThe vulnerabilities are listed below -\n\nCVE-2025-32819 (CVSS score: 8.8) - A vulnerability in SMA100 allows a remote authenticated attacker with SSL-VPN user privileges to bypass the path traversal checks and delete an",
    ),
    Article(
        link="https://thehackernews.com/2025/05/qilin-leads-april-2025-ransomware-spike.html",
        title="Qilin Ransomware Ranked Highest in April 2025 with 72 Data Leak Disclosures",
        description='Threat actors with ties to the Qilin ransomware family have leveraged malware known as SmokeLoader along with a previously undocumented .NET compiled loader codenamed NETXLOADER as part of a campaign observed in November 2024.\n"NETXLOADER is a new .NET-based loader that plays a critical role in cyber attacks," Trend Micro researchers Jacob Santos, Raymart Yambot, John Rainier Navato, Sarah Pearl',
    ),
    Article(
        link="https://thehackernews.com/2025/05/mirrorface-targets-japan-and-taiwan.html",
        title="MirrorFace Targets Japan and Taiwan with ROAMINGMOUSE and Upgraded ANEL Malware",
        description='The nation-state threat actor known as MirrorFace has been observed deploying malware dubbed ROAMINGMOUSE as part of a cyber espionage campaign directed against government agencies and public institutions in Japan and Taiwan.\nThe activity, detected by Trend Micro in March 2025, involved the use of spear-phishing lures to deliver an updated version of a backdoor called ANEL.\n"The ANEL file from',
    ),
    Article(
        link="https://thehackernews.com/2025/05/russian-hackers-using-clickfix-fake.html",
        title="Russian Hackers Using ClickFix Fake CAPTCHA to Deploy New LOSTKEYS Malware",
        description='The Russia-linked threat actor known as COLDRIVER has been observed distributing a new malware called LOSTKEYS as part of an espionage-focused campaign using ClickFix-like social engineering lures.\n"LOSTKEYS is capable of stealing files from a hard-coded list of extensions and directories, along with sending system information and running processes to the attacker," the Google Threat',
    ),
    Article(
        link="https://thehackernews.com/2025/05/cisco-patches-cve-2025-20188-100-cvss.html",
        title="Cisco Patches CVE-2025-20188 (10.0 CVSS) in IOS XE That Enables Root Exploits via JWT",
        description='Cisco has released software fixes to address a maximum-severity security flaw in its IOS XE Wireless Controller that could enable an unauthenticated, remote attacker to upload arbitrary files to a susceptible system.\nThe vulnerability, tracked as CVE-2025-20188, has been rated 10.0 on the CVSS scoring system.\n"This vulnerability is due to the presence of a hard-coded JSON Web Token (JWT) on an',
    ),
    Article(
        link="https://thehackernews.com/2025/05/europol-shuts-down-six-ddos-for-hire.html",
        title="Europol Shuts Down Six DDoS-for-Hire Services Used in Global Attacks",
        description='Europol has announced the takedown of distributed denial of service (DDoS)-for-hire services that were used to launch thousands of cyber-attacks across the world.\nIn connection with the operation, Polish authorities have arrested four individuals aged between 19 and 22 and the United States has seized nine domains that are associated with the now-defunct platforms.\n"The suspects are believed to',
    ),
    Article(
        link="https://thehackernews.com/2025/05/sysaid-patches-4-critical-flaws.html",
        title="SysAid Patches 4 Critical Flaws Enabling Pre-Auth RCE in On-Premise Version",
        description="Cybersecurity researchers have disclosed multiple security flaw in the on-premise version of SysAid IT support software that could be exploited to achieve pre-authenticated remote code execution with elevated privileges.\nThe vulnerabilities, tracked as CVE-2025-2775, CVE-2025-2776, and CVE-2025-2777, have all been described as XML External Entity (XXE) injections, which occur when an attacker is",
    ),
    Article(
        link="https://thehackernews.com/2025/05/reevaluating-sses-technical-gap.html",
        title="Reevaluating SSEs: A Technical Gap Analysis of Last-Mile Protection",
        description="Security Service Edge (SSE) platforms have become the go-to architecture for securing hybrid work and SaaS access. They promise centralized enforcement, simplified connectivity, and consistent policy control across users and devices.\nBut there's a problem: they stop short of where the most sensitive user activity actually happens—the browser.\nThis isn’t a small omission. It’s a structural",
    ),
    Article(
        link="https://thehackernews.com/2025/05/play-ransomware-exploited-windows-cve.html",
        title="Play Ransomware Exploited Windows CVE-2025-29824 as Zero-Day to Breach U.S. Organization",
        description="Threat actors with links to the Play ransomware family exploited a recently patched security flaw in Microsoft Windows as a zero-day as part of an attack targeting an unnamed organization in the United States.\nThe attack, per the Symantec Threat Hunter Team, part of Broadcom, leveraged CVE-2025-29824, a privilege escalation flaw in the Common Log File System (CLFS) driver. It was patched by",
    ),
    Article(
        link="https://thehackernews.com/2025/05/researchers-uncover-malware-in-fake.html",
        title="Researchers Uncover Malware in Fake Discord PyPI Package Downloaded 11,500+ Times",
        description="Cybersecurity researchers have discovered a malicious package on the Python Package Index (PyPI) repository that masquerades as a seemingly harmless Discord-related utility but incorporates a remote access trojan.\nThe package in question is discordpydebug, which was uploaded to PyPI on March 21, 2022. It has been downloaded 11,574 times and continues to be available on the open-source registry.",
    ),
    Article(
        link="https://thehackernews.com/2025/05/nso-group-fined-168m-for-targeting-1400.html",
        title="NSO Group Fined $168M for Targeting 1,400 WhatsApp Users With Pegasus Spyware",
        description="A federal jury on Tuesday decided that NSO Group must pay Meta-owned WhatsApp WhatsApp approximately $168 million in monetary damages, more than four months after a federal judge ruled that the Israeli company violated U.S. laws by exploiting WhatsApp servers to deploy Pegasus spyware, targeting over 1,400 individuals globally.\nWhatsApp originally filed the lawsuit against NSO Group in 2019,",
    ),
}


RELEVANT_ARTICLES = {
    Article(
        link="https://thehackernews.com/2025/05/fake-security-plugin-on-wordpress.html",
        title="Fake Security Plugin on WordPress Enables Remote Admin Access for Attackers",
        description='Cybersecurity researchers have shed light on a new campaign targeting WordPress sites that disguises the malware as a security plugin.\nThe plugin, which goes by the name "WP-antymalwary-bot.php," comes with a variety of features to maintain access, hide itself from the admin dashboard, and execute remote code.\n"Pinging functionality that can report back to a command-and-control (C&amp;C) server',
    ),
    Article(
        link="https://thehackernews.com/2025/04/critical-commvault-command-center-flaw.html",
        title="Critical Commvault Command Center Flaw Enables Attackers to Execute Code Remotely",
        description='A critical security flaw has been disclosed in the Commvault Command Center that could allow arbitrary code execution on affected installations.\nThe vulnerability, tracked as CVE-2025-34028, carries a CVSS score of 9.0 out of a maximum of 10.0.\n"A critical security vulnerability has been identified in the Command Center installation, allowing remote attackers to execute arbitrary code without',
    ),
    Article(
        link="https://thehackernews.com/2025/05/malicious-npm-packages-infect-3200.html",
        title="Malicious npm Packages Infect 3,200+ Cursor Users With Backdoor, Steal Credentials",
        description="Cybersecurity researchers have flagged three malicious npm packages that are designed to target the Apple macOS version of Cursor, a popular artificial intelligence (AI)-powered source code editor.\n\"Disguised as developer tools offering 'the cheapest Cursor API,' these packages steal user credentials, fetch an encrypted payload from threat actor-controlled infrastructure, overwrite Cursor's",
    ),
    Article(
        link="https://thehackernews.com/2025/05/ottokit-wordpress-plugin-with-100k.html",
        title="OttoKit WordPress Plugin with 100K+ Installs Hit by Exploits Targeting Multiple Flaws",
        description='A second security flaw impacting the OttoKit (formerly SureTriggers) WordPress plugin has come under active exploitation in the wild.\nThe vulnerability, tracked as CVE-2025-27007 (CVSS score: 9.8), is a privilege escalation bug impacting all versions of the plugin prior to and including version 1.0.82.&nbsp;\n"This is due to the create_wp_connection() function missing a capability check and',
    ),
    Article(
        link="https://thehackernews.com/2025/04/hackers-exploit-critical-craft-cms.html",
        title="Hackers Exploit Critical Craft CMS Flaws; Hundreds of Servers Likely Compromised",
        description="Threat actors have been observed exploiting two newly disclosed critical security flaws in Craft CMS in zero-day attacks to breach servers and gain unauthorized access.\nThe attacks, first observed by Orange Cyberdefense SensePost on February 14, 2025, involve chaining the below vulnerabilities -\n\nCVE-2024-58136 (CVSS score: 9.0) - An improper protection of alternate path flaw in the Yii PHP",
    ),
    Article(
        link="https://thehackernews.com/2025/05/commvault-confirms-hackers-exploited.html",
        title="Commvault Confirms Hackers Exploited CVE-2025-3928 as Zero-Day in Azure Breach",
        description='Enterprise data backup platform Commvault has revealed that an unknown nation-state threat actor breached its Microsoft Azure environment by exploiting CVE-2025-3928 but emphasized there is no evidence of unauthorized data access.\n"This activity has affected a small number of customers we have in common with Microsoft, and we are working with those customers to provide assistance," the company',
    ),
    Article(
        link="https://thehackernews.com/2025/05/new-chrome-vulnerability-enables-cross.html",
        title="New Chrome Vulnerability Enables Cross-Origin Data Leak via Loader Referrer Policy",
        description='Google on Wednesday released updates to address four security issues in its Chrome web browser, including one for which it said there exists an exploit in the wild.\nThe high-severity vulnerability, tracked as CVE-2025-4664 (CVSS score: 4.3), has been characterized as a case of insufficient policy enforcement in a component called Loader.\n"Insufficient policy enforcement in Loader in Google',
    ),
}
