---
title: Send TheHive alerts to Slack channels
description: Automatically notify your security team in Slack when new alerts are created in TheHive, with rich formatting and quick action buttons.
tags:
  - alerts
  - notifications
  - slack
  - automation
  - thehive
difficulty: beginner
---

# Send TheHive alerts to Slack channels

This use-case shows how to automatically send notifications to Slack when new alerts are created in TheHive.

## Overview

When a new alert is created in TheHive, this workflow will:
1. Format the alert information with rich Slack blocks
2. Post to a designated Slack channel
3. Include quick action buttons for common responses
4. Provide a direct link to the alert in TheHive

## Prerequisites

1. **Slack Workspace Access**
   - Admin access to create a Slack app
   - Permission to add apps to channels

2. **Slack App Setup**
   - Create a new Slack app in your workspace
   - Enable Incoming Webhooks
   - Add the webhook to your desired channel
   - Copy the webhook URL

3. **TheHive Setup**
   - Access to Notifications settings
   - Permission to create new notifications

## Configuration Steps

### 1. Create Slack Webhook

1. Go to https://api.slack.com/apps
2. Click **Create New App** → **From scratch**
3. Name your app (e.g., "TheHive Alerts")
4. Select your workspace
5. Navigate to **Incoming Webhooks**
6. Activate Incoming Webhooks
7. Click **Add New Webhook to Workspace**
8. Select the channel for alerts (e.g., `#security-alerts`)
9. Copy the webhook URL (looks like `https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXX`)

### 2. Configure TheHive Notification

1. Log in to TheHive
2. Navigate to **Admin organization** → **Notifications**
3. Create a new notification with:
   - **Event**: Alert created
   - **Notifier**: Webhook
   - **Webhook URL**: Your Slack webhook URL
   - **Message Template**: Use Slack Block Kit format

### 3. Test the Integration

Create a test alert in TheHive and verify it appears in your Slack channel.

## Example Slack Message Format

```json
{
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "🚨 New Security Alert"
      }
    },
    {
      "type": "section",
      "fields": [
        {
          "type": "mrkdwn",
          "text": "*Title:*\nSuspicious Login Activity"
        },
        {
          "type": "mrkdwn",
          "text": "*Severity:*\nHigh"
        },
        {
          "type": "mrkdwn",
          "text": "*Source:*\nCrowdStrike Falcon"
        },
        {
          "type": "mrkdwn",
          "text": "*Tags:*\nmalware, endpoint"
        }
      ]
    },
    {
      "type": "actions",
      "elements": [
        {
          "type": "button",
          "text": {
            "type": "plain_text",
            "text": "View in TheHive"
          },
          "url": "https://thehive.example.com/alert/12345"
        }
      ]
    }
  ]
}
```

## Benefits

✅ **Real-time notifications** - Team knows immediately when alerts arrive  
✅ **Rich formatting** - Slack blocks make information easy to read  
✅ **Quick access** - Direct links to TheHive for investigation  
✅ **Team awareness** - Everyone in the channel sees critical alerts  
✅ **Mobile notifications** - Team members get alerts on their phones

## Next Steps

- Set up different channels for different alert severities
- Add interactive buttons for common actions
- Integrate with Cortex responders for automated responses
- Create slash commands for querying TheHive from Slack
