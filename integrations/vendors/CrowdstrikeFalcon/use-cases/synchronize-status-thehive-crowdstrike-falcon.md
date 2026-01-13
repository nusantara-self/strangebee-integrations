---
title: Synchronise status between TheHive alerts/cases and CrowdStrike detections/incidents
description: Keep case/alert status in sync between TheHive and CrowdStrike Falcon using notifications and the CrowdStrikeFalcon_Sync responder.
tags: 
  - status
  - sync
  - crowdstrike
  - thehive
  - automation
---
# Tutorial: Synchronize Alert and Case Statuses from TheHive to CrowdStrike Falcon

<!-- md:license Platinum -->

In this tutorial, we're going to install and configure the Cortex responder *[Status Sync](https://thehive-project.github.io/Cortex-Analyzers/responders/CrowdstrikeFalcon/#crowdstrikefalcon_sync){target=_blank}*.

By the end, you’ll have a setup that automatically keeps alert and case statuses in sync between TheHive and CrowdStrike Falcon, so that your investigations stay aligned across both platforms.

!!! warning "Prerequisites"
    This tutorial assumes that you've already configured the ingestion of CrowdStrike Falcon detections and incidents into TheHive as alerts using [one of the available methods](crowdstrike-falcon-integrations.md#alert-ingestion).

!!! note "One-way sync"
    This synchronization only works from TheHive to CrowdStrike Falcon. If you want to sync statuses the other way around, you’ll need to implement a polling mechanism using an [alert feeder](../../thehive/user-guides/organization/configure-organization/manage-feeders/about-feeders.md).

!!! info "Status mapping"

    | TheHive stage  | CrowdStrike detection status                          | CrowdStrike incident status                          |
    | ----------- | ------------------------------------ | ------------------------------------ |
    | *New*       | *new*  | *20*  |
    | *In progress*       | *in_progress* | *30*  |
    | *Closed*    | *closed* | *40*  |

!!! tip "More integration options"
    For the complete list of integration options between CrowdStrike Falcon and TheHive, see [CrowdStrike Falcon Integration with TheHive](crowdstrike-falcon-integrations.md).

## Step 1: Create custom fields in TheHive

<!-- md:permission `manageCase/update` --> <!-- md:permission `manageAlert/update` -->

To make the link between TheHive and CrowdStrike Falcon, we’ll start by [creating two custom fields](../../thehive/administration/custom-fields/create-a-custom-field.md) that will hold detection and incident IDs.

1. {% include-markdown "includes/entities-management-view-go-to.md" %}

2. {% include-markdown "includes/custom-fields-tab-go-to.md" %}

3. Select :fontawesome-solid-plus:.

4. In the **Adding a custom field** drawer, enter the following information:

    **- Display name \***: *csfalcon-alert-id*

    **- Technical name \***: By default, the technical name is automatically generated from the display name.

    **- Description \***: *To store CrowdStrike Falcon detection IDs*

    **- Group \***: Select an existing group name or enter a new one to create a group. It organizes related custom fields when searching and appears as a tab in cases and alerts.

    **- Type \***: *string*

5. Select **Confirm custom field creation**.

6. Select :fontawesome-solid-plus: again.

7. In the **Adding a custom field** drawer, enter the following information:

    **- Display name \***: *csfalcon-incident-id*

    **- Technical name \***: By default, the technical name is automatically generated from the display name.

    **- Description \***: *To store CrowdStrike Falcon incident IDs*

    **- Group \***: Select an existing group name or enter a new one to create a group. It organizes related custom fields when searching and appears as a tab in cases and alerts.

    **- Type \***: *string*

8. Select **Confirm custom field creation**.

## Step 2: Enable and configure the Status Sync responder in Cortex

<!-- md:permission `orgAdmin` -->

Now let’s enable and configure the *CrowdStrikeFalcon_Sync_1_0* responder in Cortex.

1. Go to the **Organization** view.

2. Select the **Responders** tab.

3. Select **Enable** next to *CrowdStrikeFalcon_HostContainment_1_0*.

4. Select **Edit** next to *CrowdStrikeFalcon_HostContainment_1_0*.

5. In the **Edit responder CrowdStrikeFalcon_HostContainment_1_0** drawer, enter the required details as described in the [Cortex Neurons documentation](https://thehive-project.github.io/Cortex-Analyzers/responders/CrowdstrikeFalcon/#crowdstrikefalcon_sync){target=_blank}.

The responder is now ready to run and synchronize statuses each time a change is detected in TheHive.

## Step 3: Create a notification in TheHive to trigger the responder

<!-- md:permission `manageConfig` -->

The last step is to automate the sync by [triggering the responder](../../thehive/user-guides/organization/configure-organization/manage-notifications/create-a-notification.md) when alert or case statuses change.

1. {% include-markdown "includes/organization-view-go-to.md" %}

2. {% include-markdown "includes/notifications-tab-go-to.md" %}

3. Select :fontawesome-solid-plus:.

4. In the **Add notification** drawer, enter the name of your notification.

    !!! warning "Unique name"
        This name must be unique, as two notifications can't have the same name.

5. Select the *FilteredEvent* trigger.

6. Enter the following custom filter that activates when the stage of a case or alert linked to a CrowdStrike Falcon detection, incident, or both is updated:

    ```json
    {
        "_and": [
            {
                "_is": {
                    "action": "update"
                }
            },
            {
                "_or": [
                    {
                        "_is": {
                            "objectType": "Alert"
                        }
                    },
                    {
                        "_is": {
                            "objectType": "Case"
                        }
                    }
                ]
            },
            {
                "_contains": {
                    "details.stage": ""
                }
            },
            {
                "_or": [
                    {
                        "_contains": {
                            "context.customFieldValues.csfalcon-alert-id": ""
                        }
                    },
                    {
                        "_contains": {
                            "context.customFieldValues.csfalcon-incident-id": ""
                        }
                    }
                ]
            }
        ]
    }
    ```

7. Select the *RunResponder* notifier, then choose *CrowdStrikeFalcon_Sync_1_0* from the list.

8. Select **Confirm**.

Your system is now set up to synchronize statuses from TheHive to CrowdStrike Falcon whenever alert or case statuses are changed.

<h2>Next steps</h2>

* [Cortex Responders GitHub repository](https://github.com/TheHive-Project/Cortex-Analyzers/tree/master/responders/CrowdstrikeFalcon){target=_blank}