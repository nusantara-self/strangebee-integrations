---
title: Synchronise status between TheHive alerts/cases and CrowdStrike detections/incidents
description: Keep case/alert status in sync between TheHive and CrowdStrike Falcon using notifications and the CrowdStrikeFalcon_Sync responder.
tags: 
  - status
  - sync
  - crowdstrike
  - thehive
  - automation
difficulty: intermediate
---
# Synchronise status between TheHive alerts/cases and CrowdStrike detections/incidents

This use-case presents a way to sync alert/cases statuses from TheHive with Crowdstrike's detections and incidents.

> In this particular case, it is push-only sync (TheHive → Falcon). To pull changes the other way, add a polling script or Function, such as with the Alert Feeder feature.

---
## 1. Pre-requisites

1. **CrowdStrike Falcon Setup**:
   - Log in to your CrowdStrike Falcon tenant.
   - Navigate to **Support and resources > Resources and tools > API clients and keys**.
   - Create an **API Client** with the required permissions for `CrowdstrikeFalcon_Sync` responder:
     - **Alerts**: Read, Write
     - **Incidents**: Read, Write

2. **TheHive Setup** (for `CrowdstrikeFalcon_Sync`):
   - Log in to TheHive.
   - Navigate to **Admin organization > Entities Management > Custom fields**.
   - Create the following **custom fields**:
     - `csfalcon-alert-id` (type: **string**) – to store CrowdStrike Falcon alert IDs.
     - `csfalcon-incident-id` (type: **string**) – to store CrowdStrike Falcon incident IDs.

3. **Cortex Setup**
   - Log in to Cortex.
   - Navigate to **Organization > Responders**.
   - Enable and configure `CrowdStrikeFalcon_Sync_1_0` *(don't forget to set up the correct base_url region)*

## 2.1 Notification - Trigger

Create a Notification in TheHive, that triggers on case/alert's status stage change, which contains a linked CRWD alert or incident (or both).

Filtered event - **CRWDAlertOrCaseStageChange**

Trigger condition: This triggers when a case or alert, which contains a linked CRWD alert or incident (or both), has its stage updated

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

## 2.2 Notifier

* Enable notification with notifier `RunResponder`

* Add `CrowdStrikeFalcon_Sync_1_0` for `thehive:case` & `thehive:alert`

## 3. Summary  
On every stage change of a CrowdStrike-linked alert or case, the **CrowdStrikeFalcon_Sync** responder pushes the new stage to Falcon.  
> **Direction:** TheHive → Falcon (**one-way**). Add a polling script if you also want Falcon → TheHive.

---

### Stage ↔ Status Mapping

| TheHive Stage | Detection status | Incident status |
| ------------- | ---------------- | --------------- |
| New           | `new`            | `20`            |
| In-Progress   | `in_progress`    | `30`            |
| Closed        | `closed`         | `40`            |
