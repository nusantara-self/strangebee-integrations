---
title: Interactive incident response with Slack slash commands
description: Manage TheHive cases and tasks directly from Slack using slash commands and interactive modals for faster incident response.
tags:
  - incident-response
  - slack
  - slash-commands
  - interactive
  - thehive
difficulty: advanced
---

# Interactive incident response with Slack slash commands

Respond to security incidents without leaving Slack by using slash commands to interact with TheHive.

## Overview

This advanced use-case enables your team to:
- Query TheHive cases and alerts from Slack
- Create new cases with interactive modals
- Update case status and assignments
- Add observables and tasks
- Run Cortex analyzers

## Prerequisites

1. **Slack App with slash commands**
2. **TheHive API access**
3. **Middleware service** (Node.js, Python, etc.) to bridge Slack ↔ TheHive
4. **HTTPS endpoint** for receiving Slack commands

## Example Commands

```
/thehive search <query>          - Search cases and alerts
/thehive case create             - Create a new case (opens modal)
/thehive case <id> status        - Update case status
/thehive case <id> assign @user  - Assign case to team member
/thehive observable add <value>  - Add observable to current case
```

## Benefits

✅ **Faster response** - Act without switching applications  
✅ **Team collaboration** - Everyone sees actions in channel  
✅ **Reduced friction** - Lower barrier to taking action  
✅ **Audit trail** - All actions logged in both Slack and TheHive

---

*This is an advanced integration requiring custom development. Contact your security team for implementation details.*
