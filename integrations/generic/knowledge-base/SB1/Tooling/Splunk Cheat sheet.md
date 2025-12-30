---
title: Splunk Search Cheat Sheet
category: Tooling
---

# Splunk Search Cheat Sheet

- Find failed logins: `index=windows EventCode=4625`
- Search by IP: `index=network src_ip=1.2.3.4`
- Top talkers: `index=network | top src_ip`