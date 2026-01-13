---
title: Phishing Email – Incident Response Procedure
category: Procedures
---

# Phishing Email – Incident Response Procedure

## Purpose

Standard procedure for handling reported or detected phishing emails.

## Steps

1. **Validate the reported email:**  
   Check sender, headers, attachments, and URLs.
2. **Isolate the impacted mailbox:**  
   If compromise is suspected, disable forwarding and change credentials.
3. **Search for similar emails:**  
   Use SIEM to find other recipients or similar content.
4. **Block malicious indicators:**  
   Update mail gateway and endpoint protection as needed.
5. **Notify users:**  
   Contact affected users, provide guidance, and reset passwords if needed.
6. **Document all actions:**  
   Log all steps and findings in the relevant TheHive case.

---

**References:**  
- [How to analyze email headers (link)](https://www.howto.com/email-headers)
- [Phishing awareness tips (PDF)](phishing_awareness_tips.pdf)