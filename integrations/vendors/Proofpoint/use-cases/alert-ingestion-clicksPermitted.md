---
title: Ingest Proofpoint ClicksPermitted Events into TheHive Using an Alert Feeder
description: Ingest Proofpoint TAP clicksPermitted events as TheHive alerts to track and respond to users who clicked on malicious links that were not blocked by Proofpoint and may require investigation.
tags: [proofpoint, tap, clicksPermitted, alert-ingestion]
thehive_version_required : "5.5"
license_required : "platinum"
linked_to : ["integrations/vendors/Proofpoint/thehive/functions/function_Feeder_alertFromProofpoint_clicksPermitted.js"]
---
# Tutorial: Ingest Proofpoint ClicksPermitted Events into TheHive Using an Alert Feeder

<!-- md:permission `manageConfig` --> <!-- md:integration Native --> <!-- md:version 5.5 --> <!-- md:license Platinum -->

{% include-markdown "includes/alert-feeder-proofpoint-tap-not-tested-live.md" %}

In this tutorial, we're going to configure an alert feeder that ingests Proofpoint Targeted Attack Protection (TAP) `clicksPermitted` events as TheHive alerts.

By the end, you'll have a working setup to track and respond to users who clicked on malicious links that weren't blocked by Proofpoint.

!!! tip "More integration options"
    For the complete list of integration options between Proofpoint and TheHive, see [Proofpoint Integration with TheHive](proofpoint-integrations.md).

{% include-markdown "includes/tap-service-credentials.md" %}

## Step 2: Create an alert feeder in TheHive

To ingest Proofpoint `clicksPermitted` events into TheHive, you need to [create an alert feeder](../../thehive/user-guides/organization/configure-organization/manage-feeders/create-a-feeder.md) that queries the Proofpoint SIEM API and transforms the results into alerts.

1. {% include-markdown "includes/organization-view-go-to.md" %}

2. {% include-markdown "includes/connectors-tab-organization-go-to.md" %}

3. In the **General settings** section, enter the following information:

    **- Name**: *ProofpointTAPAlertIngestion-clicksPermitted*

    **- Interval**: How often the alert feeder sends requests to the external system.

    !!! warning "Define the interval carefully based on your reactivity requirements"
        Make sure the interval is shorter than the processing time to avoid potential issues, but not too short to prevent excessive requests to the API.

    **- Request timeout time**: The maximum time, in seconds, the alert feeder waits for a response before timing out.

    **- Request response max size**: The maximum response size, in megabytes, that the alert feeder accepts from the external system.

    **- Description**: *Ingests Proofpoint TAP clicksPermitted events from the last hour as actionable alerts in TheHive*

4. In the **HTTP request** section, enter the following information:

    **- Method**: *GET*

    **- URL**: *https://tap-api-v2.proofpoint.com/v2/siem/clicks/permitted?format=json&sinceSeconds=3600*

    **- Auth type**: *Basic*

    **- Auth username**: Your Proofpoint TAP service principal.

    **- Auth password**: Your Proofpoint TAP service secret.

5. Select **Test connection** to verify the connection to the external system.

6. In the **Create function** section, enter the following information:

    !!! info "Feeder function"
        Once created, the function is automatically added to the [functions list](../../thehive/user-guides/organization/configure-organization/manage-functions/about-functions.md) with the type *feeder*.

    **- Function name**: *ProofpointClicksPermitted*

    **- Description**: *This function processes each clicksPermitted event and creates a unique TheHive alert. Alerts are deduplicated using the Proofpoint GUID field*

    **- Definition**

    Use this function definition:

    ```javascript
    // Name: ProofpointClicksPermitted
    // Type: Feeder
    // Desc: This function processes each clicksPermitted event and creates a unique TheHive alert. Alerts are deduplicated using the Proofpoint GUID field.

    function handle(input, context) {

        // Example JSON array returned by the Proofpoint TAP SIEM API:
        // const testInput = {
        //   "clicksPermitted": [
        //     {
        //       "campaignId": "46e01b8a-c899-404d-bcd9-189bb393d1a7",
        //       "classification": "MALWARE",
        //       "clickIP": "192.0.2.1",
        //       "clickTime": "2016-06-24T19:17:44.000Z",
        //       "GUID": "b27dbea0-87d5-463b-b93c-4e8b708289ce",
        //       "id": "8c8b4895-a277-449f-r797-547e3c89b25a",
        //       "messageID": "8c6cfedd-3050-4d65-8c09-c5f65c38da81",
        //       "recipient": "bruce.wayne@pharmtech.zz",
        //       "sender": "9facbf452def2d7efc5b5c48cdb837fa@badguy.zz",
        //       "senderIP": "192.0.2.255",
        //       "threatID": "61f7622167144dba5e3ae4480eeee78b23d66f7dfed970cfc3d086cc0dabdf50",
        //       "threatTime": "2016-06-24T19:17:46.000Z",
        //       "threatURL": "https://threatinsight.proofpoint.com/#/73aa0499-dfc8-75eb-1de8-a471b24a2e75/threat/u/61f7622167144dba5e3ae4480eeee78b23d66f7dfed970cfc3d086cc0dabdf50",
        //       "threatStatus": "active",
        //       "url": "http://badguy.zz/",
        //       "userAgent": "Mozilla/5.0(WindowsNT6.1;WOW64;rv:27.0)Gecko/20100101Firefox/27.0"
        //     }
        //   ]
        // };
        // const events = testInput.clicksPermitted || [];

        const events = input.clicksPermitted || [];
        events.forEach((event) => {
            // Deduplication
            const filters = [
                {
                    _name: "filter",
                    _and: [
                    { _field: "sourceRef", _value: event.id }
                    ]
                }
            ];
            if (context.alert.find(filters).length < 1) {
                // Compose alert details
                const title = `[Proofpoint] Permitted Malicious Click - ${event.recipient}`;
                const description =
                    `A user clicked on a malicious URL that was NOT blocked by Proofpoint TAP.\n\n` +
                    `**User:** ${event.recipient}\n` +
                    `**Sender:** ${event.sender}\n` +
                    `**URL:** ${event.url}\n` +
                    `**Classification:** ${event.classification}\n` +
                    `**Click Time:** ${event.clickTime}\n` +
                    `**Threat Status:** ${event.threatStatus}\n` +
                    `**Threat URL:** ${event.threatURL}\n` +
                    `**User Agent:** ${event.userAgent}\n` +
                    `\nFull Event JSON:\n\`\`\`json\n${JSON.stringify(event, null, 2)}\n\`\`\``;

                // Observables
                const observables = [
                    { dataType: "mail", data: event.recipient, tags: ["recipient"] },
                    { dataType: "mail", data: event.sender, tags: ["sender"] },
                    { dataType: "url", data: event.url, tags: ["clicked"] },
                    { dataType: "url", data: event.threatURL, tags: ["threat", "proofpoint"] },
                    { dataType: "ip", data: event.clickIP, tags: ["clickIP"] },
                    { dataType: "ip", data: event.senderIP, tags: ["senderIP"] },
                    { dataType: "user-agent", data: event.userAgent, tags: [] }
                ];

                // MITRE ATT&CK mapping
                const mitreMapping = {
                    "MALWARE": {
                    tag: "T1204.001",
                    tactic: "execution" // https://attack.mitre.org/techniques/T1204/001/
                    },
                    "PHISHING": {
                    tag: "T1566.002",
                    tactic: "phishing" // https://attack.mitre.org/techniques/T1566/002/
                    }
                };

                const eventClassification = (event.classification || "").toUpperCase();
                const matched = mitreMapping[eventClassification] ? [mitreMapping[eventClassification]] : [];

                // Alert date
                const dateStr = event.threatTime || event.clickTime;
                const eventTimestamp = dateStr ? new Date(dateStr).getTime() : Date.now();

                // Build procedures array
                const procedures = matched.map(mitre => ({
                    patternId: mitre.tag,
                    occurDate: eventTimestamp,
                    ...(mitre.tactic ? { tactic: mitre.tactic } : {})
                }));

                // Tags
                const tags = [
                    "Proofpoint",
                    event.classification,
                    event.threatStatus,
                    "campaignId:" + (event.campaignId || "N/A"),
                    ...matched.map(mitre => "TTP:" + mitre.tag)
                ];

                // Build alert
                const alert = {
                    "type": "event",
                    "source": "ProofpointTAP-clicksPermitted",
                    "sourceRef": event.id,
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

At this point, your alert feeder should be operational and TheHive will start ingesting `clicksPermitted` events as alerts.

<h2>Next steps</h2>

* [Ingest Proofpoint messagesDelivered Events into TheHive Using an Alert Feeder](ingest-proofpoint-messagesdelivered-events.md)
