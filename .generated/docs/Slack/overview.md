# Slack

![Slack Logo](https://raw.githubusercontent.com/nusantara-self/strangebee-integrations/refs/heads/develop/integrations/vendors/Slack/assets/logo.png)

Slack is a is a team collaboration platform that provides channels, direct messaging, file sharing, and an app ecosystem for workflows and incident response.

**Category:** Collaboration  
**Homepage:** https://slack.com  
**Tags:** communication, collaboration, notifications, chat

## Subscription Information

- **Registration Required:** Yes
- **Subscription Required:** No
- **Free Subscription Available:** Yes

## Responders (2)

### Slack_SyncChannel `v1.0`
Syncs Slack channel conversations to TheHive task logs. Imports messages chronologically with file attachments for traceability.

- **Data Types:** `thehive:case`
- **Configuration:** [.upstream/cortex/responders/Slack/Slack_SyncChannel.json](.upstream/cortex/responders/Slack/Slack_SyncChannel.json)

### Slack_CreateChannel `v1.0`
Creates a Slack channel for a TheHive case, invites participants, and optionally posts a case summary and description.

- **Data Types:** `thehive:case`
- **Configuration:** [.upstream/cortex/responders/Slack/Slack_CreateChannel.json](.upstream/cortex/responders/Slack/Slack_CreateChannel.json)

---

## Statistics

- **Total Analyzers:** 0
- **Total Responders:** 2
- **Total Functions:** 0
- **Total Integrations:** 2

---

*This file is auto-generated from the integration manifest. Do not edit manually.*
