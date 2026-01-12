# Free & Local Integrations

Integrations that are either free to use or run locally without external dependencies.

## 📊 Summary

- **Total Free/Local Analyzers:** 65
- **Total Free/Local Responders:** 7
- **Total:** 72

**Legend:**
- 🆓 Free subscription available
- 🏠 Local integration (no external API required)

## 🔍 Analyzers

### AbuseIPDB `v1.1` 🆓

**Vendor:** [AbuseIPDB](/vendors/AbuseIPDB/overview)
**Data Types:** `ip`

Checks an IP against AbuseIPDB for abuse score, categories, and recent reports.

---

### AIL_OnionLookup `v1.0` 🆓

**Vendor:** [AILOnionLookup](/vendors/AILOnionLookup/overview)
**Data Types:** `domain`, `url`, `fqdn`

Checks the existence of Tor hidden services and retrieving their associated metadata. Onion-lookup relies on an AIL instance to obtain the metadata.

---

### OTXQuery `v2.0` 🆓

**Vendor:** [AlienVault OTX](/vendors/OTXQuery/overview)
**Data Types:** `url`, `domain`, `file`, `hash`, `ip`

Query AlienVault OTX for IPs, domains, URLs, or file hashes.

---

### CIRCLHashlookup `v1.1` 🆓

**Vendor:** [CIRCLHashlookup](/vendors/CIRCLHashlookup/overview)
**Data Types:** `hash`

CIRCL hashlookup uses a public API to lookup hash values against databases of known good files

---

### CIRCLPassiveDNS `v2.0` 🆓

**Vendor:** [CIRCLPassiveDNS](/vendors/CIRCLPassiveDNS/overview)
**Data Types:** `domain`, `url`, `ip`

Check CIRCL's Passive DNS for a given domain or URL.

---

### CIRCLPassiveSSL `v2.0` 🆓

**Vendor:** [CIRCLPassiveSSL](/vendors/CIRCLPassiveSSL/overview)
**Data Types:** `ip`, `certificate_hash`, `hash`

Check CIRCL's Passive SSL for a given IP address or a X509 certificate hash.

---

### CIRCLVulnerabilityLookup `v1.0` 🆓

**Vendor:** [CIRCLVulnerabilityLookup](/vendors/CIRCLVulnerabilityLookup/overview)
**Data Types:** `cve`, `cve_id`, `vuln`, `vuln_id`, `vulnerability`, `vulnerability_id`, `cveid`, `other`

Queries the CIRCL Vulnerability Lookup API to retrieve detailed information on security vulnerabilities, including CVEs, severity (CVSS), exploit prediction (EPSS), affected products, advisories, and recent sightings.

---

### Crowdsec_Analyzer `v1.1` 🆓

**Vendor:** [CrowdSec](/vendors/Crowdsec/overview)
**Data Types:** `ip`

Query Crowdsec API

---

### Crt_sh_Transparency_Logs `v1.0` 🆓

**Vendor:** [Crtsh](/vendors/Crtsh/overview)
**Data Types:** `domain`

Query domains against the certificate transparency lists available at crt.sh.

---

### CyberCrime-Tracker `v1.0` 🆓

**Vendor:** [CyberCrime-Tracker](/vendors/CyberCrime-Tracker/overview)
**Data Types:** `domain`, `fqdn`, `ip`, `url`, `other`

Search cybercrime-tracker.net for C2 servers.

---

### DShield_lookup `v1.0` 🆓

**Vendor:** [DShield](/vendors/DShield/overview)
**Data Types:** `ip`

Query the SANS ISC DShield API to check for an IP address reputation.

---

### EchoTrail `v1.0` 🆓

**Vendor:** [EchoTrail](/vendors/EchoTrail/overview)
**Data Types:** `hash`, `filename`

EchoTrail Insights takes a Windows filename or hash and provides several unique pieces of analytical context including prevalence & rank scores, process ancestry, behavioral analysis, and security analysis.

---

### Elasticsearch_Analysis `v1.0` 🆓

**Vendor:** [Elasticsearch](/vendors/Elasticsearch/overview)
**Data Types:** `url`, `domain`, `ip`, `hash`, `filename`, `fqdn`

Search for IoCs in Elasticsearch

---

### EmailRep `v1.0` 🆓

**Vendor:** [EmailRep](/vendors/EmailRep/overview)
**Data Types:** `mail`

emailrep.io lookup.

---

### JA4_FoxIO `v1.0` 🆓

**Vendor:** [FoxIO](/vendors/FoxIO/overview)
**Data Types:** `user-agent`, `ja4-fingerprint`

JA4 Fingerprint analysis with FoxIO Database

---

### GreyNoise `v3.2` 🆓

**Vendor:** [GreyNoise](/vendors/GreyNoise/overview)
**Data Types:** `ip`

Determine whether an IP has known scanning activity using GreyNoise.

---

### Hashdd_Detail `v2.0` 🆓

**Vendor:** [Hashdd](/vendors/Hashdd/overview)
**Data Types:** `hash`

Determine whether a hash is good or bad; if good then list what it is.

---

### Hashdd_Status `v2.0` 🆓

**Vendor:** [Hashdd](/vendors/Hashdd/overview)
**Data Types:** `hash`

Determine whether a hash is good or bad.

---

### Hunterio_DomainSearch `v1.0` 🆓

**Vendor:** [Hunter.io](/vendors/Hunterio/overview)
**Data Types:** `domain`, `fqdn`

hunter.io is a service to find email addresses from a domain.

---

### Inoitsu `v1.0` 🆓

**Vendor:** [Inoitsu](/vendors/Inoitsu/overview)
**Data Types:** `mail`

Query Inoitsu for a compromised email address.

---

### IntezerCommunity `v1.0` 🆓

**Vendor:** [IntezerCommunity](/vendors/IntezerCommunity/overview)
**Data Types:** `file`, `hash`

Analyze a possible malicious file with Intezer Analyzer

---

### isMalicious_GetReport `v1.0` 🆓

**Vendor:** [isMalicious](/vendors/isMalicious/overview)
**Data Types:** `ip`, `domain`, `fqdn`

Check if an IP address or domain is malicious using isMalicious.com threat intelligence. Returns risk score, threat categories, reputation data, and detection sources.

---

### Jupyter_Run_Notebook_Analyzer `v1.0` 🆓

**Vendor:** [Jupyter](/vendors/Jupyter/overview)
**Data Types:** `domain`, `hostname`, `ip`, `url`, `fqdn`, `uri_path`, `user-agent`, `hash`, `mail`, `mail_subject`, `registry`, `regexp`, `other`, `filename`, `mail-subject`

Execute a parameterized notebook in Jupyter

---

### Lookyloo_Screenshot `v1.0` 🆓

**Vendor:** [Lookyloo](/vendors/Lookyloo/overview)
**Data Types:** `url`, `domain`, `fqdn`, `ip`

Take a screenshot of an url, domain, FQDN or IP and report all HTTP redirections

---

### MalwareBazaar `v1.0` 🆓

**Vendor:** [MalwareBazaar](/vendors/MalwareBazaar/overview)
**Data Types:** `hash`

Search hashes on MalwareBazaar.

---

### Malwares_GetReport `v1.0` 🆓

**Vendor:** [Malwares](/vendors/Malwares/overview)
**Data Types:** `file`, `hash`, `domain`, `ip`

Get the latest Malwares report for a file, hash, domain or an IP address.

---

### Malwares_Scan `v1.0` 🆓

**Vendor:** [Malwares](/vendors/Malwares/overview)
**Data Types:** `file`

Use Malwares' API to scan a file or URL.

---

### MSDefenderOffice365_SafeLinksDecoder.json `v1.0` 🆓

**Vendor:** [Microsoft Defender for Office 365](/vendors/MSDefenderOffice365/overview)
**Data Types:** `url`

Decodes Office 365 ATP Safe Links to extract original URLs. Supports url observables containing safelinks.protection.outlook.com domains.

---

### MISP `v2.1` 🆓

**Vendor:** [MISP](/vendors/MISP/overview)
**Data Types:** `domain`, `ip`, `url`, `fqdn`, `uri_path`, `user-agent`, `hash`, `mail`, `mail_subject`, `registry`, `regexp`, `other`, `filename`, `mail-subject`

Query multiple MISP instances for events containing an observable.

---

### NERD `v1.1` 🆓

**Vendor:** [NERD](/vendors/NERD/overview)
**Data Types:** `ip`

Get Reputation score and other basic information from Network Entity Reputation Database (NERD)

---

### ONYPHE_ASM `v1.1` 🆓

**Vendor:** [ONYPHE](/vendors/Onyphe/overview)
**Data Types:** `ip`, `domain`, `fqdn`, `hash`

Manage an attack surface from The Hive using ONYPHE riskscan category

---

### ONYPHE_Ctiscan `v1.0` 🆓

**Vendor:** [ONYPHE](/vendors/Onyphe/overview)
**Data Types:** `ip`, `domain`, `fqdn`, `hash`, `autonomous-system`, `other`

Query ONYPHE Ctiscan threat hunting data for open services (takes ip, domain, fqdn, autonomous-system or hash.)

---

### ONYPHE_Search `v1.1` 🆓

**Vendor:** [ONYPHE](/vendors/Onyphe/overview)
**Data Types:** `ip`, `domain`, `fqdn`, `hash`

Retrieve results from ONYPHE Search API for a given ip, domain, fqdn or hash (sha256 TLS fingerprint) from specified category

---

### ONYPHE_Summary_API `v1.2` 🆓

**Vendor:** [ONYPHE](/vendors/Onyphe/overview)
**Data Types:** `ip`, `domain`, `fqdn`

Retrieve summary information Onyphe has for given ip, domain, or fqdn.

---

### ONYPHE_Vulnscan `v1.1` 🆓

**Vendor:** [ONYPHE](/vendors/Onyphe/overview)
**Data Types:** `ip`, `domain`, `fqdn`, `hash`

Retrieve vulnerability data from ONYPHE vulnscan category for a given ip, domain, fqdn or hash (sha256 TLS fingerprint)

---

### PhishingInitiative_Lookup `v2.0` 🆓

**Vendor:** [PhishingInitiative](/vendors/PhishingInitiative/overview)
**Data Types:** `url`

Use Phishing Initiative to check if a URL is a verified phishing site.

---

### PhishingInitiative_Scan `v1.0` 🆓

**Vendor:** [PhishingInitiative](/vendors/PhishingInitiative/overview)
**Data Types:** `url`

Use Phishing Initiative to scan a URL.

---

### PhishTank_CheckURL `v2.1` 🆓

**Vendor:** [PhishTank](/vendors/PhishTank/overview)
**Data Types:** `url`

Use PhishTank to check if a URL is a verified phishing site.

---

### Shodan_DNSResolve `v1.0` 🆓

**Vendor:** [Shodan](/vendors/Shodan/overview)
**Data Types:** `domain`, `fqdn`

Retrieve domain resolutions on Shodan.

---

### Shodan_Host `v1.0` 🆓

**Vendor:** [Shodan](/vendors/Shodan/overview)
**Data Types:** `ip`

Retrieve key Shodan information on an IP address.

---

### Shodan_Host_History `v1.0` 🆓

**Vendor:** [Shodan](/vendors/Shodan/overview)
**Data Types:** `ip`

Retrieve Shodan history scan results  for an IP address.

---

### Shodan_InfoDomain `v1.0` 🆓

**Vendor:** [Shodan](/vendors/Shodan/overview)
**Data Types:** `domain`, `fqdn`

Retrieve key Shodan information on a domain.

---

### Shodan_ReverseDNS `v1.0` 🆓

**Vendor:** [Shodan](/vendors/Shodan/overview)
**Data Types:** `ip`

Retrieve ip reverse DNS resolutions on Shodan.

---

### Shodan_Search `v2.0` 🆓

**Vendor:** [Shodan](/vendors/Shodan/overview)
**Data Types:** `other`

Search query on Shodan

---

### Splunk_Search_Domain_FQDN `v3.0` 🆓

**Vendor:** [Splunk](/vendors/Splunk/overview)
**Data Types:** `domain`, `fqdn`

Execute a savedsearch on a Splunk instance with a domain or a FQDN as argument

---

### Splunk_Search_File_Filename `v3.0` 🆓

**Vendor:** [Splunk](/vendors/Splunk/overview)
**Data Types:** `file`, `filename`

Execute a savedsearch on a Splunk instance with a file/filename as argument

---

### Splunk_Search_Hash `v3.0` 🆓

**Vendor:** [Splunk](/vendors/Splunk/overview)
**Data Types:** `hash`

Execute a savedsearch on a Splunk instance with a hash as argument

---

### Splunk_Search_IP `v3.0` 🆓

**Vendor:** [Splunk](/vendors/Splunk/overview)
**Data Types:** `ip`

Execute a savedsearch on a Splunk instance with an IP as argument

---

### Splunk_Search_Mail_Email `v3.0` 🆓

**Vendor:** [Splunk](/vendors/Splunk/overview)
**Data Types:** `mail`, `email`

Execute a savedsearch on a Splunk instance with a mail/email as argument

---

### Splunk_Search_Mail_Subject `v3.0` 🆓

**Vendor:** [Splunk](/vendors/Splunk/overview)
**Data Types:** `mail_subject`, `mail-subject`

Execute a savedsearch on a Splunk instance with a mail subject as argument

---

### Splunk_Search_Other `v3.0` 🆓

**Vendor:** [Splunk](/vendors/Splunk/overview)
**Data Types:** `other`

Execute a savedsearch on a Splunk instance with an unidentified data as argument

---

### Splunk_Search_Registry `v3.0` 🆓

**Vendor:** [Splunk](/vendors/Splunk/overview)
**Data Types:** `registry`

Execute a savedsearch on a Splunk instance with a registry data as argument

---

### Splunk_Search_URL_URI_Path `v3.0` 🆓

**Vendor:** [Splunk](/vendors/Splunk/overview)
**Data Types:** `url`, `uri_path`

Execute a savedsearch on a Splunk instance with an URL or a URI path as argument

---

### Splunk_Search_User `v3.0` 🆓

**Vendor:** [Splunk](/vendors/Splunk/overview)
**Data Types:** `other`

Execute a savedsearch on a Splunk instance with a user ID as argument

---

### Splunk_Search_User_Agent `v3.0` 🆓

**Vendor:** [Splunk](/vendors/Splunk/overview)
**Data Types:** `user-agent`

Execute a savedsearch on a Splunk instance with a user agent as argument

---

### TorBlutmagie `v1.0` 🆓

**Vendor:** [TorBlutmagie](/vendors/TorBlutmagie/overview)
**Data Types:** `ip`, `domain`, `fqdn`

Query https://torstatus.rueckgr.at/query_export.php/Tor_query_EXPORT.csv (formerly TorBlutmagie) for TOR exit nodes IP addresses or names.

---

### Triage `v2.0` 🆓

**Vendor:** [Triage](/vendors/Triage/overview)
**Data Types:** `ip`, `url`, `file`

Submit artifacts to the Recorded Future Triage sandbox service. This analyzer requires a paid subscription for the Private and Recorded Future sandboxes.

---

### UrlDNA_New_Scan `v0.1.0` 🆓

**Vendor:** [urlDNA.io](/vendors/urlDNA.io/overview)
**Data Types:** `url`

Perform a new scan on urlDNA.io

---

### UrlDNA_Search `v0.1.0` 🆓

**Vendor:** [urlDNA.io](/vendors/urlDNA.io/overview)
**Data Types:** `ip`, `domain`, `url`

Perform a search on urlDNA.io for IPs, domains or URLs

---

### URLhaus `v2.0` 🆓

**Vendor:** [URLhaus](/vendors/URLhaus/overview)
**Data Types:** `domain`, `fqdn`, `url`, `hash`, `ip`

Search domains, IPs, URLs or hashes on URLhaus.

---

### Urlscan.io_Scan `v0.1.0` 🆓

**Vendor:** [URLScan.io](/vendors/Urlscan.io/overview)
**Data Types:** `url`, `domain`, `fqdn`

Scan URLs on urlscan.io

---

### Urlscan.io_Search `v0.1.1` 🆓

**Vendor:** [URLScan.io](/vendors/Urlscan.io/overview)
**Data Types:** `ip`, `domain`, `hash`, `fqdn`, `url`

Search IPs, domains, hashes or URLs on urlscan.io

---

### Vulners_CVE `v1.0` 🆓

**Vendor:** [Vulners](/vendors/Vulners/overview)
**Data Types:** `cve`

Get information about CVE from powerful Vulners database.

---

### Vulners_IOC `v1.0` 🆓

**Vendor:** [Vulners](/vendors/Vulners/overview)
**Data Types:** `url`, `domain`, `ip`

Get information from the RST Threat Feed, which integrated with Vulners, for a domain, url or an IP address.

---

### Yara `v3.0` 🆓

**Vendor:** [YARA](/vendors/Yara/overview)
**Data Types:** `file`

Check files against YARA rules, either from local filesystem or from one or multiple GitHub repositories. NOTE: Performance & execution time may be much longer according to the number of rules checked.

---

## ⚡ Responders

### Jupyter_Run_Notebook_Responder `v1.0` 🆓

**Vendor:** [Jupyter](/vendors/Jupyter/overview)
**Data Types:** `thehive:case`, `thehive:case_artifact`, `thehive:alert`, `thehive:case_task`, `thehive:case_task_log`

Execute a parameterized notebook in Jupyter

---

### MSDefenderOffice365_block `v1.0` 🆓

**Vendor:** [Microsoft Defender for Office 365](/vendors/MSDefenderOffice365/overview)
**Data Types:** `thehive:case_artifact`

Add entries to the Tenant Allow/Block List in the Microsoft 365 Defender

---

### MSDefenderOffice365_unblock `v1.0` 🆓

**Vendor:** [Microsoft Defender for Office 365](/vendors/MSDefenderOffice365/overview)
**Data Types:** `thehive:case_artifact`

Add entries to the Tenant Allow/Block List in the Microsoft 365 Defender

---

### n8n `v1.0` 🆓

**Vendor:** [n8n](/vendors/n8n/overview)
**Data Types:** `thehive:case`, `thehive:alert`, `thehive:case_artifact`, `thehive:case_task`, `thehive:case_task_log`

Send data to n8n via webhook

---

### Slack_CreateChannel `v1.0` 🆓

**Vendor:** [Slack](/vendors/Slack/overview)
**Data Types:** `thehive:case`

Creates a Slack channel for a TheHive case, invites participants, and optionally posts a case summary and description.

---

### Slack_SyncChannel `v1.0` 🆓

**Vendor:** [Slack](/vendors/Slack/overview)
**Data Types:** `thehive:case`

Syncs Slack channel conversations to TheHive task logs. Imports messages chronologically with file attachments for traceability.

---

### Telegram `v1.0` 🆓

**Vendor:** [Telegram](/vendors/Telegram/overview)
**Data Types:** `thehive:case`

Send a message to Telegram with information from TheHive case

---

---

*This catalog is auto-generated. Do not edit manually.*
