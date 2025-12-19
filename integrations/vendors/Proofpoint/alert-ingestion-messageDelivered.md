---
title: Ingest Proofpoint MessagesDelivered Events into TheHive Using an Alert Feeder
description: Ingest Proofpoint TAP messagesDelivered events as TheHive alerts to track and respond to threats that have reached user mailboxes and may require investigation.
tags: [proofpoint, tap, messagesDelivered, alert-ingestion]
---
# Tutorial: Ingest Proofpoint MessagesDelivered Events into TheHive Using an Alert Feeder

<!-- md:permission `manageConfig` --> <!-- md:integration Native --> <!-- md:version 5.5 --> <!-- md:license Platinum -->

{% include-markdown "includes/alert-feeder-proofpoint-tap-not-tested-live.md" %}

In this tutorial, we're going to configure an alert feeder that ingests Proofpoint Targeted Attack Protection (TAP) `messagesDelivered` events as TheHive alerts.

By the end, you'll have a working setup to track threats that reached user mailboxes and may require investigation or response.

!!! tip "More integration options"
    For the complete list of integration options between Proofpoint and TheHive, see [Proofpoint Integration with TheHive](proofpoint-integrations.md).

{% include-markdown "includes/tap-service-credentials.md" %}

## Step 2: Create an alert feeder in TheHive

To ingest Proofpoint `messagesDelivered` events into TheHive, you need to [create an alert feeder](../../thehive/user-guides/organization/configure-organization/manage-feeders/create-a-feeder.md) that queries the Proofpoint SIEM API and transforms the results into alerts.

1. {% include-markdown "includes/organization-view-go-to.md" %}

2. {% include-markdown "includes/connectors-tab-organization-go-to.md" %}

3. In the **General settings** section, enter the following information:

    **- Name**: *ProofpointTAPAlertIngestion-messagesDelivered*

    **- Interval**: How often the alert feeder sends requests to the external system.

    !!! warning "Define the interval carefully based on your reactivity requirements"
        Make sure the interval is shorter than the processing time to avoid potential issues, but not too short to prevent excessive requests to the API.

    **- Request timeout time**: The maximum time, in seconds, the alert feeder waits for a response before timing out.

    **- Request response max size**: The maximum response size, in megabytes, that the alert feeder accepts from the external system.

    **- Description**: *Ingests Proofpoint TAP messagesDelivered events from the last hour as actionable alerts in TheHive*

4. In the **HTTP request** section, enter the following information:

    **- Method**: *GET*

    **- URL**: *https://tap-api-v2.proofpoint.com/v2/siem/messages/delivered?format=json&sinceSeconds=3600*

    **- Auth type**: *Basic*

    **- Auth username**: Your Proofpoint TAP service principal.

    **- Auth password**: Your Proofpoint TAP service secret.

5. Select **Test connection** to verify the connection to the external system.

6. In the **Create function** section, enter the following information:

    !!! info "Feeder function"
        Once created, the function is automatically added to the [functions list](../../thehive/user-guides/organization/configure-organization/manage-functions/about-functions.md) with the type *feeder*.

    **- Function name**: *ProofpointMessagesDelivered*

    **- Description**: *This function processes each messagesDelivered event and creates a unique TheHive alert. Alerts are deduplicated using the Proofpoint GUID field*

    **- Definition**

    Use this function definition:

    ```javascript
    // Name: ProofpointMessagesDelivered
    // Type: Feeder
    // Desc: This function processes each messagesDelivered event and creates a unique TheHive alert. Alerts are deduplicated using the Proofpoint GUID field.

    // Example JSON array returned by the Proofpoint TAP SIEM API:
    // const testInput = {
    // {
    //  "messagesDelivered": [
    //    {
    //      "GUID": "a2345678-bcde-5f01-2345-6789abcdef01",
    //      "QID": "r2FNwRHF004120",
    //      "fromAddress": "attacker@evil.com",
    //      "headerFrom": "\"Fake CEO\" <attacker@evil.com>",
    //      "headerTo": "\"Finance\" <finance@company.com>",
    //      "subject": "Immediate Transfer Required",
    //      "impostorScore": 99,
    //      "malwareScore": 0,
    //      "phishScore": 98,
    //      "spamScore": 30,
    //      "threatsInfoMap": [
    //        {
    //          "threat": "http://badsite.example.com",
    //          "threatID": "def456abc123",
    //          "threatStatus": "active",
    //          "threatTime": "2025-05-29T07:00:00Z"
    //        }
    //      ],
    //      "messageTime": "2025-05-29T07:00:00Z"
    //    }
    //  ]
    // }
    // const events = testInput.messagesDelivered || [];

    function extractEmailAndName(address) {
        // Handles "Name <email@domain.com>" or just "email@domain.com"
        if (!address) return { email: "", name: "" };
        const match = address.match(/^(.*)<(.+?)>$/);
        if (match) {
            // Remove quotes and trim whitespace
            return { email: match[2].trim(), name: match[1].replace(/["']/g, '').trim() };
        }
        return { email: address.trim(), name: "" };
    }

    function handle(input, context) {
        const events = input.messagesDelivered || [];
        events.forEach((event) => {
            // Deduplication
            const filters = [
                {
                    _name: "filter",
                    _and: [
                    { _field: "sourceRef", _value: event.GUID }
                    ]
                }
            ];
            if (context.alert.find(filters).length < 1) {
                // Compose alert details
                const subject = event.subject || "(no subject)";
                const title = `[Proofpoint] Delivered Suspicious Message - ${subject}`;
                const description =
                    `A suspicious message was delivered to a user's mailbox by Proofpoint TAP.\n\n` +
                    `**From:** ${event.fromAddress}\n` +
                    `**To:** ${event.headerTo}\n` +
                    `**Subject:** ${event.subject}\n` +
                    `**Impostor Score:** ${event.impostorScore}\n` +
                    `**Malware Score:** ${event.malwareScore}\n` +
                    `**Phish Score:** ${event.phishScore}\n` +
                    `**Spam Score:** ${event.spamScore}\n` +
                    `**Threats:**\n${(event.threatsInfoMap || []).map(t => `- ${t.threat} (ID: ${t.threatID}, Status: ${t.threatStatus})`).join('\n')}\n` +
                    `**Message Time:** ${event.messageTime}\n` +
                    `\nFull Event JSON:\n\`\`\`json\n${JSON.stringify(event, null, 2)}\n\`\`\``;

                // Prepare mail observables with name in tags
                const fromInfo = extractEmailAndName(event.fromAddress);
                const headerFromInfo = extractEmailAndName(event.headerFrom);
                const headerToInfo = extractEmailAndName(event.headerTo);

                const observables = [
                    ...(event.threatsInfoMap || []).map(t => ({
                        dataType: "url",
                        data: t.threat,
                        tags: ["threat", t.threatStatus]
                    })),
                    { dataType: "mail", data: fromInfo.email, tags: ["from", ...(fromInfo.name ? [fromInfo.name] : [])] },
                    { dataType: "mail", data: headerToInfo.email, tags: ["to", ...(headerToInfo.name ? [headerToInfo.name] : [])] },
                    { dataType: "mail", data: headerFromInfo.email, tags: ["headerFrom", ...(headerFromInfo.name ? [headerFromInfo.name] : [])] },
                    ...(event.headerTo ? [{ dataType: "mail", data: headerToInfo.email, tags: ["recipient", ...(headerToInfo.name ? [headerToInfo.name] : [])] }] : []),
                    ...(event.headerFrom ? [{ dataType: "mail", data: headerFromInfo.email, tags: ["sender", ...(headerFromInfo.name ? [headerFromInfo.name] : [])] }] : [])
                ];

                // MITRE ATT&CK mapping (basic example)
                let mitreTag = null;
                let tactic = null;
                if ((event.phishScore || 0) > 70) {
                    mitreTag = "T1566.002"; // Spearphishing Link
                    tactic = "phishing";
                } else if ((event.malwareScore || 0) > 70) {
                    mitreTag = "T1204.002"; // Malicious File
                    tactic = "execution";
                }
                const dateStr = (event.threatsInfoMap && event.threatsInfoMap[0] && event.threatsInfoMap[0].threatTime) || event.messageTime;
                const eventTimestamp = dateStr ? new Date(dateStr).getTime() : Date.now();

                const procedures = mitreTag ? [{
                    patternId: mitreTag,
                    occurDate: eventTimestamp,
                    ...(tactic ? { tactic: tactic } : {})
                }] : [];

                // Tags
                const tags = [
                    "Proofpoint",
                    "messagesDelivered",
                    event.subject,
                    ...(event.threatsInfoMap || []).map(t => t.threatStatus),
                    ...(mitreTag ? ["TTP:" + mitreTag] : [])
                ];

                // Build alert
                const alert = {
                    "type": "event",
                    "source": "ProofpointTAP-messagesDelivered",
                    "sourceRef": event.GUID,
                    "title": title,
                    "description": description,
                    "tags": tags,
                    "observables": observables,
                    "date": eventTimestamp,
                    "procedures": procedures
                };

                context.alert.create(alert);
            }
        });
    }
    ```

7. {% include-markdown "includes/test-function.md" %}

8. Select **Confirm**.

For more details, see the [Proofpoint SIEM API official documentation](https://help.proofpoint.com/Threat_Insight_Dashboard/API_Documentation/SIEM_API){target=_blank}.

At this point, your alert feeder should be operational and TheHive will start ingesting `messagesDelivered` events as alerts.

<h2>Next steps</h2>

* [Ingest Proofpoint clicksPermitted Events into TheHive Using an Alert Feeder](ingest-proofpoint-clickspermitted-events.md)