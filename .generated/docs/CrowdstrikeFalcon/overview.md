# CrowdStrike Falcon

![CrowdStrike Falcon Logo](https://raw.githubusercontent.com/nusantara-self/strangebee-integrations/refs/heads/develop/integrations/vendors/CrowdstrikeFalcon/assets/logo.png)

CrowdStrike Falcon is a cloud-native endpoint protection platform that provides real-time threat detection, prevention, and response capabilities

**Category:** EDR  
**Homepage:** https://www.crowdstrike.com  
**Tags:** endpoint-protection, threat-detection, incident-response, cloud-native, edr

## Subscription Information

- **Registration Required:** Yes
- **Subscription Required:** Yes
- **Free Subscription Available:** No

## Analyzers (10)

### CrowdstrikeFalcon_Sandbox_Win7 `v1.0`
Send a file to CrowdstrikeFalcon Sandbox

- **Data Types:** `file`
- **Configuration:** [.upstream/cortex/analyzers/CrowdstrikeFalcon/CrowdstrikeFalcon_Sandbox_Win7.json](https://raw.githubusercontent.com/nusantara-self/strangebee-integrations/refs/heads/develop/.upstream/cortex/analyzers/CrowdstrikeFalcon/CrowdstrikeFalcon_Sandbox_Win7.json)

### CrowdstrikeFalcon_Sandbox_Win7_64 `v1.0`
Send a file to CrowdstrikeFalcon Sandbox

- **Data Types:** `file`
- **Configuration:** [.upstream/cortex/analyzers/CrowdstrikeFalcon/CrowdstrikeFalcon_Sandbox_Win7_64.json](https://raw.githubusercontent.com/nusantara-self/strangebee-integrations/refs/heads/develop/.upstream/cortex/analyzers/CrowdstrikeFalcon/CrowdstrikeFalcon_Sandbox_Win7_64.json)

### CrowdstrikeFalcon_getDeviceAlerts `v1.0`
Get Device alerts from Crowdstrike Falcon

- **Data Types:** `hostname`
- **Configuration:** [.upstream/cortex/analyzers/CrowdstrikeFalcon/CrowdstrikeFalcon_getDeviceAlerts.json](https://raw.githubusercontent.com/nusantara-self/strangebee-integrations/refs/heads/develop/.upstream/cortex/analyzers/CrowdstrikeFalcon/CrowdstrikeFalcon_getDeviceAlerts.json)

### CrowdstrikeFalcon_Sandbox_Android `v1.0`
Send a file to CrowdstrikeFalcon Sandbox

- **Data Types:** `file`
- **Configuration:** [.upstream/cortex/analyzers/CrowdstrikeFalcon/CrowdstrikeFalcon_Sandbox_Android.json](https://raw.githubusercontent.com/nusantara-self/strangebee-integrations/refs/heads/develop/.upstream/cortex/analyzers/CrowdstrikeFalcon/CrowdstrikeFalcon_Sandbox_Android.json)

### CrowdstrikeFalcon_Sandbox_MacOS `v1.0`
Send a file to CrowdstrikeFalcon Sandbox

- **Data Types:** `file`
- **Configuration:** [.upstream/cortex/analyzers/CrowdstrikeFalcon/CrowdstrikeFalcon_Sandbox_MacOS.json](https://raw.githubusercontent.com/nusantara-self/strangebee-integrations/refs/heads/develop/.upstream/cortex/analyzers/CrowdstrikeFalcon/CrowdstrikeFalcon_Sandbox_MacOS.json)

### CrowdstrikeFalcon_Sandbox_Win11 `v1.0`
Send a file to CrowdstrikeFalcon Sandbox

- **Data Types:** `file`
- **Configuration:** [.upstream/cortex/analyzers/CrowdstrikeFalcon/CrowdstrikeFalcon_Sandbox_Win11.json](https://raw.githubusercontent.com/nusantara-self/strangebee-integrations/refs/heads/develop/.upstream/cortex/analyzers/CrowdstrikeFalcon/CrowdstrikeFalcon_Sandbox_Win11.json)

### CrowdstrikeFalcon_GetDeviceVulnerabilities `v1.0`
Get device vulnerabilities from hostname

- **Data Types:** `hostname`
- **Configuration:** [.upstream/cortex/analyzers/CrowdstrikeFalcon/CrowdstrikeFalcon_GetDeviceVulnerabilities.json](https://raw.githubusercontent.com/nusantara-self/strangebee-integrations/refs/heads/develop/.upstream/cortex/analyzers/CrowdstrikeFalcon/CrowdstrikeFalcon_GetDeviceVulnerabilities.json)

### CrowdstrikeFalcon_Sandbox_Win10 `v1.0`
Send a file to CrowdstrikeFalcon Sandbox

- **Data Types:** `file`
- **Configuration:** [.upstream/cortex/analyzers/CrowdstrikeFalcon/CrowdstrikeFalcon_Sandbox_Win10.json](https://raw.githubusercontent.com/nusantara-self/strangebee-integrations/refs/heads/develop/.upstream/cortex/analyzers/CrowdstrikeFalcon/CrowdstrikeFalcon_Sandbox_Win10.json)

### CrowdstrikeFalcon_getDeviceDetails `v1.0`
Get device information from Crowdstrike Falcon

- **Data Types:** `hostname`
- **Configuration:** [.upstream/cortex/analyzers/CrowdstrikeFalcon/CrowdstrikeFalcon_getDeviceDetails.json](https://raw.githubusercontent.com/nusantara-self/strangebee-integrations/refs/heads/develop/.upstream/cortex/analyzers/CrowdstrikeFalcon/CrowdstrikeFalcon_getDeviceDetails.json)

### CrowdstrikeFalcon_Sandbox_Linux `v1.0`
Send a file to CrowdstrikeFalcon Sandbox

- **Data Types:** `file`
- **Configuration:** [.upstream/cortex/analyzers/CrowdstrikeFalcon/CrowdstrikeFalcon_Sandbox_Linux.json](https://raw.githubusercontent.com/nusantara-self/strangebee-integrations/refs/heads/develop/.upstream/cortex/analyzers/CrowdstrikeFalcon/CrowdstrikeFalcon_Sandbox_Linux.json)

---

## Responders (9)

### CrowdStrikeFalcon_unhideHost `v1.0`
This action will restore a host. Detection reporting will resume after the host is restored

- **Data Types:** `thehive:case_artifact`
- **Configuration:** [.upstream/cortex/responders/CrowdstrikeFalcon/CrowdstrikeFalcon_unhideHost.json](https://raw.githubusercontent.com/nusantara-self/strangebee-integrations/refs/heads/develop/.upstream/cortex/responders/CrowdstrikeFalcon/CrowdstrikeFalcon_unhideHost.json)

### CrowdStrikeFalcon_suppressDetections `v1.0`
Supress detections for the host.

- **Data Types:** `thehive:case_artifact`
- **Configuration:** [.upstream/cortex/responders/CrowdstrikeFalcon/CrowdstrikeFalcon_suppressDetections.json](https://raw.githubusercontent.com/nusantara-self/strangebee-integrations/refs/heads/develop/.upstream/cortex/responders/CrowdstrikeFalcon/CrowdstrikeFalcon_suppressDetections.json)

### CrowdStrikeFalcon_HostContainment `v1.0`
This action contains the host, which stops any network communications to locations other than the CrowdStrike cloud and IPs specified in your containment policy

- **Data Types:** `thehive:case_artifact`
- **Configuration:** [.upstream/cortex/responders/CrowdstrikeFalcon/CrowdstrikeFalcon_containHost.json](https://raw.githubusercontent.com/nusantara-self/strangebee-integrations/refs/heads/develop/.upstream/cortex/responders/CrowdstrikeFalcon/CrowdstrikeFalcon_containHost.json)

### CrowdStrikeFalcon_hideHost `v1.0`
This action will delete a host. After the host is deleted, no new detections for that host will be reported via UI or APIs

- **Data Types:** `thehive:case_artifact`
- **Configuration:** [.upstream/cortex/responders/CrowdstrikeFalcon/CrowdstrikeFalcon_hideHost.json](https://raw.githubusercontent.com/nusantara-self/strangebee-integrations/refs/heads/develop/.upstream/cortex/responders/CrowdstrikeFalcon/CrowdstrikeFalcon_hideHost.json)

### CrowdStrikeFalcon_LiftContainmentHost `v1.0`
This action lifts containment on the host, which returns its network communications to normal

- **Data Types:** `thehive:case_artifact`
- **Configuration:** [.upstream/cortex/responders/CrowdstrikeFalcon/CrowdstrikeFalcon_liftContainmentHost.json](https://raw.githubusercontent.com/nusantara-self/strangebee-integrations/refs/heads/develop/.upstream/cortex/responders/CrowdstrikeFalcon/CrowdstrikeFalcon_liftContainmentHost.json)

### CrowdStrikeFalcon_Sync `v1.0`
Sync TheHive status back to CS Alerts or Incidents

- **Data Types:** `thehive:case`, `thehive:alert`
- **Configuration:** [.upstream/cortex/responders/CrowdstrikeFalcon/CrowdStrikeFalcon_Sync.json](https://raw.githubusercontent.com/nusantara-self/strangebee-integrations/refs/heads/develop/.upstream/cortex/responders/CrowdstrikeFalcon/CrowdStrikeFalcon_Sync.json)

### CrowdStrikeFalcon_AddIOC `v1.0`
Add IOC to IoC Management on Crowdstrike - supports domain, url, IPs & different kind of hashes

- **Data Types:** `thehive:case_artifact`
- **Configuration:** [.upstream/cortex/responders/CrowdstrikeFalcon/CrowdStrikeFalcon_AddIOC.json](https://raw.githubusercontent.com/nusantara-self/strangebee-integrations/refs/heads/develop/.upstream/cortex/responders/CrowdstrikeFalcon/CrowdStrikeFalcon_AddIOC.json)

### CrowdStrikeFalcon_unsuppressDetections `v1.0`
Allow detections for the host.

- **Data Types:** `thehive:case_artifact`
- **Configuration:** [.upstream/cortex/responders/CrowdstrikeFalcon/CrowdstrikeFalcon_unsuppressDetection.json](https://raw.githubusercontent.com/nusantara-self/strangebee-integrations/refs/heads/develop/.upstream/cortex/responders/CrowdstrikeFalcon/CrowdstrikeFalcon_unsuppressDetection.json)

### CrowdStrikeFalcon_RemoveIOC `v1.0`
remove IOC from IoC Management on Crowdstrike

- **Data Types:** `thehive:case_artifact`
- **Configuration:** [.upstream/cortex/responders/CrowdstrikeFalcon/CrowdStrikeFalcon_removeIOC.json](https://raw.githubusercontent.com/nusantara-self/strangebee-integrations/refs/heads/develop/.upstream/cortex/responders/CrowdstrikeFalcon/CrowdStrikeFalcon_removeIOC.json)

---

## Functions (1)

### CRWDAlertIngestion `v1.0.0`
Ingests CrowdstrikeFalcon Alerts, also processes observables & TTPs.

- **Kind:** function
- **Mode:** Enabled
- **File:** [integrations/vendors/CrowdstrikeFalcon/thehive/functions/crwd-alert-ingestion.js](https://raw.githubusercontent.com/nusantara-self/strangebee-integrations/refs/heads/develop/integrations/vendors/CrowdstrikeFalcon/thehive/functions/crwd-alert-ingestion.js)

---

## Use Cases (1)

### Synchronise status between TheHive alerts/cases and CrowdStrike detections/incidents
Keep case/alert status in sync between TheHive and CrowdStrike Falcon using notifications and the CrowdStrikeFalcon_Sync responder.

**Tags:** status, sync, crowdstrike, thehive, automation
📄 [Documentation](https://raw.githubusercontent.com/nusantara-self/strangebee-integrations/refs/heads/develop/integrations/vendors/CrowdstrikeFalcon/synchronize-status-thehive-crowdstrike-falcon.md)

---

## Statistics

- **Total Analyzers:** 10
- **Total Responders:** 9
- **Total Functions:** 1
- **Total Integrations:** 20

---

*This file is auto-generated from the integration manifest. Do not edit manually.*
