# MSDefenderEndpoints


## Subscription Information

- **Registration Required:** Yes
- **Subscription Required:** Yes
- **Free Subscription Available:** No

## Responders (8)

### MSDefender-FullVirusscan `v1.0`
Run full virus scan to machine with Microsoft Defender for Endpoints

- **Data Types:** `thehive:case_artifact`
- **Configuration:** [.upstream/cortex/responders/MSDefenderEndpoints/MSDefenderEndpoints_VirusScan.json](.upstream/cortex/responders/MSDefenderEndpoints/MSDefenderEndpoints_VirusScan.json)

### MSDefender-UnRestrictAppExecution `v1.0`
Enable execution of any application on the device

- **Data Types:** `thehive:case_artifact`
- **Configuration:** [.upstream/cortex/responders/MSDefenderEndpoints/MSDefenderEndpoints_UnRestrictAppExecution.json](.upstream/cortex/responders/MSDefenderEndpoints/MSDefenderEndpoints_UnRestrictAppExecution.json)

### MSDefender-RestrictAppExecution `v1.0`
Restrict execution of all applications on the device except a predefined set

- **Data Types:** `thehive:case_artifact`
- **Configuration:** [.upstream/cortex/responders/MSDefenderEndpoints/MSDefenderEndpoints_RestrictAppExecution.json](.upstream/cortex/responders/MSDefenderEndpoints/MSDefenderEndpoints_RestrictAppExecution.json)

### MSDefender-AutoInvestigation `v1.0`
Start an automated investigation on a device

- **Data Types:** `thehive:case_artifact`
- **Configuration:** [.upstream/cortex/responders/MSDefenderEndpoints/MSDefenderEndpoints_AutoInvestigation.json](.upstream/cortex/responders/MSDefenderEndpoints/MSDefenderEndpoints_AutoInvestigation.json)

### MSDefender-PushIOC-Alert `v2.0`
Push IOC to Defender client. Alert mode

- **Data Types:** `thehive:case_artifact`
- **Configuration:** [.upstream/cortex/responders/MSDefenderEndpoints/MSDefenderEndpoints_PushIOCAlert.json](.upstream/cortex/responders/MSDefenderEndpoints/MSDefenderEndpoints_PushIOCAlert.json)

### MSDefender-IsolateMachine `v1.0`
Isolate machine with Microsoft Defender for Endpoints

- **Data Types:** `thehive:case_artifact`
- **Configuration:** [.upstream/cortex/responders/MSDefenderEndpoints/MSDefenderEndpoints_Isolate.json](.upstream/cortex/responders/MSDefenderEndpoints/MSDefenderEndpoints_Isolate.json)

### MSDefender-PushIOC-Block `v2.0`
Push IOC to Defender client. Blocking mode

- **Data Types:** `thehive:case_artifact`
- **Configuration:** [.upstream/cortex/responders/MSDefenderEndpoints/MSDefenderEndpoints_PushIOCBlock.json](.upstream/cortex/responders/MSDefenderEndpoints/MSDefenderEndpoints_PushIOCBlock.json)

### MSDefender-UnisolateMachine `v1.0`
Unisolate machine with Microsoft Defender for Endpoints

- **Data Types:** `thehive:case_artifact`
- **Configuration:** [.upstream/cortex/responders/MSDefenderEndpoints/MSDefenderEndpoints_Unisolate.json](.upstream/cortex/responders/MSDefenderEndpoints/MSDefenderEndpoints_Unisolate.json)

---

## Statistics

- **Total Analyzers:** 0
- **Total Responders:** 8
- **Total Functions:** 0
- **Total Integrations:** 8

---

*This file is auto-generated from the integration manifest. Do not edit manually.*
