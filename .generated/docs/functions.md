# Functions Catalog

Complete list of TheHive functions available for workflow automation.

## 📊 Summary

- **Total Functions:** 13
- **Generic Functions:** 6
- **Vendor-Specific Functions:** 7
- **Vendors with Functions:** 6

## 🔧 Generic Functions

These functions are vendor-agnostic and can be used across all TheHive installations:

### assignAlert `v1.0.0`

**Type:** Notifier
**Mode:** Enabled

This function is designed to trigger on alert creation event. It automatically assignes severity High & Critical alerts to a given user

---

### assignToMe `v1.0.0`

**Type:** Action:Case
**Mode:** Enabled

This function changes the assignee of the Case and all the associated tasks to the user who launches the function

---

### automatedIgnoreSimilarityForNoisyObservables `v1.0.0`

**Type:** Notifier
**Mode:** Enabled

This function is intended to be triggered on ObservableCreated events. It automatically sets ignoreSimilarity to true for observables matching a known list of common, noisy, or non-actionable values (such as localhost, private IPs, and generic hostnames..). This reduces alert noise and avoids false correlation in TheHive. Note that it is a workaround, and such issues are better managed in your alert ingestion pipeline(s)

---

### changeImportedAlertStatus `v1.0.0`

**Type:** Notifier
**Mode:** Enabled

This function is designed to trigger on case closed event. It automatically changes imported alerts to a given custom status

---

### coldCaseAutomation `v1.0.0`

**Type:** API
**Mode:** Enabled

This function will find the "New" or "InProgress" cases that were not updated since one month. For each case, add a tag "cold-case"

---

### deleteIPObsFromAlert `v1.0.0`

**Type:** Action:Alert
**Mode:** Enabled

This function will delete all the IP Observable from an alert

---

## 🏢 Vendor-Specific Functions

### Airtable

**Vendor:** [Airtable](/vendors/Airtable/overview)

#### alertFromAirtable `v1.0.0`
**Kind:** `function`

This function creates alerts from data coming from a Airtable database. It checks the alert does not already exist, then creates the alert, and completes type, source, source-ref, title, description and tags

---

### CrowdStrike Falcon

**Vendor:** [CrowdStrike Falcon](/vendors/CrowdstrikeFalcon/overview)

#### CRWDAlertIngestion `v1.0.0`
**Kind:** `function`

Ingests CrowdstrikeFalcon Alerts, also processes observables & TTPs.

---

### JAMFProtect

**Vendor:** [JAMFProtect](/vendors/JAMFProtect/overview)

#### createAlertFromJAMFProtect `v1.0.0`
**Kind:** `function`

Ingests alerts from JAMF Protect. Extracts analytic details, host and user information, MITRE ATT&CK tags, and file/path data. The function constructs a TheHive alert, including a title, markdown-formatted description (with original alert JSON), relevant observables (IP, hostname, file, hash, URL, FQDN, URI path, user agent), MITRE ATT&CK enrichment, and a link to the JAMF alert. Handles default values and supports tagging and mapping of MITRE tactics for easier triage and investigation. For the setup in JAMF Protect, go to Configuration > Actions > *your action* > Add an HTTP data endpoint + your Authorization Header and Bearer as value

---

### JIRA

**Vendor:** [JIRA](/vendors/JIRA/overview)

#### alertFromJIRA `v1.0.0`
**Kind:** `function`

This function creates alerts from JIRA issues. It checks if the alert already exists, then creates it with type, source, source-ref, title, and description

---

### Proofpoint

**Vendor:** [Proofpoint](/vendors/Proofpoint/overview)

#### alertFeeder_ProofPoint_clicksPermitted `v1.0.0`
**Kind:** `function`

Ingests ProofPoint clicksPermitted alerts in TheHive

#### alertFeeder_ProofPoint_messageDelivered `v1.0.0`
**Kind:** `function`

Ingests ProofPoint messageDelivered alerts in TheHive

---

### Splunk

**Vendor:** [Splunk](/vendors/Splunk/overview)

#### createAlertFromSplunk `v1.0.0`
**Kind:** `function`

This function creates a TheHive Alert based on an input coming from Splunk, and matches the Splunk fields to TheHive fields. In Splunk, you'll need to configure the webhook URL to point to the TheHive function URL

---

---

*This catalog is auto-generated. Do not edit manually.*
