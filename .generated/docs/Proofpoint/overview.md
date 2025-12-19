# Proofpoint

![Proofpoint Logo](https://raw.githubusercontent.com/nusantara-self/strangebee-integrations/refs/heads/develop/integrations/vendors/Proofpoint/assets/logo.png)

Proofpoint is an enterprise email security and threat protection platform that provides advanced threat detection, URL defense, and forensic analysis capabilities

**Category:** Email Security  
**Homepage:** https://www.proofpoint.com  
**Tags:** email-security

## Analyzers (1)

### Proofpoint_Lookup `v1.0`
Check URL, file, SHA256 against Proofpoint forensics

- **Data Types:** `url`, `file`, `hash`
- **Configuration:** [.upstream/cortex/analyzers/Proofpoint/ProofPoint_Lookup.json](.upstream/cortex/analyzers/Proofpoint/ProofPoint_Lookup.json)

---

## Functions (2)

### alertFeeder_ProofPoint_messageDelivered `v1.0.0`
Ingests ProofPoint messageDelivered alerts in TheHive

- **Kind:** function
- **Mode:** Enabled
- **File:** [integrations/vendors/Proofpoint/thehive/functions/function_Feeder_alertFromProofpoint_messageDelivered](integrations/vendors/Proofpoint/thehive/functions/function_Feeder_alertFromProofpoint_messageDelivered)

### alertFeeder_ProofPoint_clicksPermitted `v1.0.0`
Ingests ProofPoint clicksPermitted alerts in TheHive

- **Kind:** function
- **Mode:** Enabled
- **File:** [integrations/vendors/Proofpoint/thehive/functions/function_Feeder_alertFromProofpoint_clicksPermitted](integrations/vendors/Proofpoint/thehive/functions/function_Feeder_alertFromProofpoint_clicksPermitted)

---

## Statistics

- **Total Analyzers:** 1
- **Total Responders:** 0
- **Total Functions:** 2
- **Total Integrations:** 3

---

*This file is auto-generated from the integration manifest. Do not edit manually.*
