---
title: Automated investigation channels for case collaboration
description: Automatically create dedicated Slack channels for each TheHive case, with team members added and updates synced in real-time.
tags:
  - collaboration
  - investigation
  - slack
  - automation
  - case-management
difficulty: intermediate
---

# Automated investigation channels for case collaboration

Create a dedicated Slack channel for each security investigation to keep all communication and updates in one place.

## Overview

When a new case is created in TheHive, this workflow:
1. Creates a dedicated Slack channel (e.g., `#case-12345-phishing-attack`)
2. Automatically adds assigned team members
3. Posts case details and observables
4. Syncs case updates to the channel
5. Archives channel when case is closed

## Key Features

- **Automatic channel creation** with case ID and title
- **Team member syncing** based on case assignments
- **Real-time updates** for case changes
- **Observable tracking** posted to channel
- **Analysis results** from Cortex analyzers
- **Channel archival** when investigation closes

## Benefits

✅ **Centralized communication** - All discussion in one place  
✅ **Context preservation** - Full investigation history  
✅ **Easy onboarding** - New team members see full context  
✅ **Searchable** - Find past investigations easily  
✅ **Integration hub** - Connect other tools to the channel

## Configuration

This requires a custom integration service that:
1. Listens to TheHive case events
2. Uses Slack API to manage channels
3. Syncs updates bidirectionally

---

*Recommended for teams handling 10+ cases per month.*
