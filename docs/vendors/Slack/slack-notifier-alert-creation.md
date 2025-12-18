---
title: Notify Slack When an Alert Is Created in TheHive
description: For each new alert in TheHive, create a Slack block message with a title, severity & link to the alert.
tags: [slack, communication, notification]
---
# Tutorial: Notify Slack When an Alert Is Created in TheHive

<!-- md:permission `manageConfig` --> <!-- md:license Platinum -->

![Slack alert creation](../images/slack-notifier-alert-creation.png)

In this tutorial, we're going to set up a notification that uses the *Slack* notifier to send a message whenever a new alert is created in TheHive.

By the end, TheHive will automatically post a Slack message that includes a link to the alert along with its type and severity.

!!! tip "More integration options"
    For the complete list of integration options between Slack and TheHive, see [Slack Integration with TheHive](slack-integrations.md).

{% include-markdown "includes/create-slack-app.md" %}

## Step 2: Add a Slack endpoint

To send messages to Slack, TheHive requires a [*Slack* endpoint](../../thehive/user-guides/organization/configure-organization/manage-endpoints/add-slack-endpoint.md). You can reuse the same endpoint across multiple notifications.

{% include-markdown "includes/add-local-slack-endpoint.md" %}

## Step 3: Create a notification in TheHive

With the endpoint in place, [create a notification](../../thehive/user-guides/organization/configure-organization/manage-notifications/create-a-notification.md) that triggers whenever an alert is created.

1. {% include-markdown "includes/organization-view-go-to.md" %}

2. {% include-markdown "includes/notifications-tab-go-to.md" %}

3. Select :fontawesome-solid-plus:.

4. In the **Add notification** drawer, enter the name of your notification: *SlackNotificationAlertCreation*

    !!! warning "Unique name"
        This name must be unique, as two notifications can't have the same name.

5. Select the *AlertCreated* trigger.

6. Select the *Slack* notifier.

7. In the **Slack** drawer, configure the following:

    **- Endpoint**: Select the endpoint you created in [Step 2](#step-2-add-a-slack-endpoint).

    **- Text template**:

    {% include-markdown "includes/notifications-variables.md" %}
    
    {% include-markdown "includes/templates-helpers.md" %}

    ```
    An alert of type *{{object.type}}* has been created :\n- Title: *{{object.title}}*\n- Severity: *{{object.severity}}*\n[Click here]({{url}}) to interact
    ```

    **- Channel**: Select the Slack channel where messages should be posted.

    **- Username**: The name that will appear as the sender of the message in Slack.

    **- Advanced settings**: Turn on advanced settings and paste the following into the Blocks template field:

    ```
    [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "🚨 New {{objectType}} Created",
                "emoji": true
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Title*: *{{object.title}}*"
            }
        },
        {
            "type": "section",
            "fields": [
                {
                "type": "mrkdwn",
                "text": "*Type*: {{object.type}}"
                },
                {
                "type": "mrkdwn",
                "text": "*Severity*: {{ severityLabel object.severity }}"
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
                        "text": "🔗 Link to {{objectType}}",
                        "emoji": true
                },
                "url": "{{url}}",
                "style": "primary"
                }
            ]
        }
    ]
    ```

8. Select **Confirm**.

At this point, the notification is ready. Each time an alert is created in TheHive, a message will automatically be posted to the selected Slack channel. You can further customize the message format of the Slack notifier using the [official Slack documentation](https://docs.slack.dev/reference/methods/chat.postMessage/){target=_blank}.

<h2>Next steps</h2>

* [Notify Slack When a Case Assignee Changes in TheHive](notify-slack-case-assignee-change.md)