# Functions Catalog

Complete list of TheHive functions available for workflow automation.

## 📊 Summary

- **Total Functions:** 13
- **Generic Functions:** 6
- **Vendor-Specific Functions:** 7
- **Vendors with Functions:** 6

## 🔧 Generic Functions

These functions are vendor-agnostic and can be used across all TheHive installations:

### [assignAlert](functions/assignalert.md) `v1.0.0`

**Type:** Notifier
**Mode:** Enabled

This function is designed to trigger on alert creation event. It automatically assignes severity High & Critical alerts to a given user

📄 [View full documentation](functions/assignalert.md)

---

### [assignToMe](functions/assigntome.md) `v1.0.0`

**Type:** Action:Case
**Mode:** Enabled

This function changes the assignee of the Case and all the associated tasks to the user who launches the function

📄 [View full documentation](functions/assigntome.md)

---

### [automatedIgnoreSimilarityForNoisyObservables](functions/automatedignoresimilarityfornoisyobservables.md) `v1.0.0`

**Type:** Notifier
**Mode:** Enabled

This function is intended to be triggered on ObservableCreated events. It automatically sets ignoreSimilarity to true for observables matching a known list of common, noisy, or non-actionable values (such as localhost, private IPs, and generic hostnames..). This reduces alert noise and avoids false correlation in TheHive. Note that it is a workaround, and such issues are better managed in your alert ingestion pipeline(s)

📄 [View full documentation](functions/automatedignoresimilarityfornoisyobservables.md)

---

### [changeImportedAlertStatus](functions/changeimportedalertstatus.md) `v1.0.0`

**Type:** Notifier
**Mode:** Enabled

This function is designed to trigger on case closed event. It automatically changes imported alerts to a given custom status

📄 [View full documentation](functions/changeimportedalertstatus.md)

---

### [coldCaseAutomation](functions/coldcaseautomation.md) `v1.0.0`

**Type:** API
**Mode:** Enabled

This function will find the "New" or "InProgress" cases that were not updated since one month. For each case, add a tag "cold-case"

📄 [View full documentation](functions/coldcaseautomation.md)

---

### [deleteIPObsFromAlert](functions/deleteipobsfromalert.md) `v1.0.0`

**Type:** Action:Alert
**Mode:** Enabled

This function will delete all the IP Observable from an alert

📄 [View full documentation](functions/deleteipobsfromalert.md)

---

## 🏢 Vendor-Specific Functions

### Airtable

**Vendor:** [Airtable](/vendors/Airtable/overview)

#### [alertFromAirtable](functions/airtable-alertfromairtable.md) `v1.0.0`
**Kind:** `function`

This function creates alerts from data coming from a Airtable database. It checks the alert does not already exist, then creates the alert, and completes type, source, source-ref, title, description and tags

📄 [View full documentation](functions/airtable-alertfromairtable.md)

---

### CrowdStrike Falcon

**Vendor:** [CrowdStrike Falcon](/vendors/CrowdstrikeFalcon/overview)

#### [CRWDAlertIngestion](functions/crowdstrike-falcon-crwdalertingestion.md) `v1.0.0`
**Kind:** `function`

Ingests CrowdstrikeFalcon Alerts, also processes observables & TTPs.

📄 [View full documentation](functions/crowdstrike-falcon-crwdalertingestion.md)

---

### JAMFProtect

**Vendor:** [JAMFProtect](/vendors/JAMFProtect/overview)

#### [createAlertFromJAMFProtect](functions/jamfprotect-createalertfromjamfprotect.md) `v1.0.0`
**Kind:** `function`

Ingests alerts from JAMF Protect. Extracts analytic details, host and user information, MITRE ATT&CK tags, and file/path data. The function constructs a TheHive alert, including a title, markdown-formatted description (with original alert JSON), relevant observables (IP, hostname, file, hash, URL, FQDN, URI path, user agent), MITRE ATT&CK enrichment, and a link to the JAMF alert. Handles default values and supports tagging and mapping of MITRE tactics for easier triage and investigation. For the setup in JAMF Protect, go to Configuration > Actions > *your action* > Add an HTTP data endpoint + your Authorization Header and Bearer as value

📄 [View full documentation](functions/jamfprotect-createalertfromjamfprotect.md)

---

### JIRA

**Vendor:** [JIRA](/vendors/JIRA/overview)

#### [alertFromJIRA](functions/jira-alertfromjira.md) `v1.0.0`
**Kind:** `function`

This function creates alerts from JIRA issues. It checks if the alert already exists, then creates it with type, source, source-ref, title, and description

📄 [View full documentation](functions/jira-alertfromjira.md)

---

### Proofpoint

**Vendor:** [Proofpoint](/vendors/Proofpoint/overview)

#### [alertFeeder_ProofPoint_clicksPermitted](functions/proofpoint-alertfeeder_proofpoint_clickspermitted.md) `v1.0.0`
**Kind:** `function`

Ingests ProofPoint clicksPermitted alerts in TheHive

📄 [View full documentation](functions/proofpoint-alertfeeder_proofpoint_clickspermitted.md)

#### [alertFeeder_ProofPoint_messageDelivered](functions/proofpoint-alertfeeder_proofpoint_messagedelivered.md) `v1.0.0`
**Kind:** `function`

Ingests ProofPoint messageDelivered alerts in TheHive

📄 [View full documentation](functions/proofpoint-alertfeeder_proofpoint_messagedelivered.md)

---

### Splunk

**Vendor:** [Splunk](/vendors/Splunk/overview)

#### [createAlertFromSplunk](functions/splunk-createalertfromsplunk.md) `v1.0.0`
**Kind:** `function`

This function creates a TheHive Alert based on an input coming from Splunk, and matches the Splunk fields to TheHive fields. In Splunk, you'll need to configure the webhook URL to point to the TheHive function URL

📄 [View full documentation](functions/splunk-createalertfromsplunk.md)

---

---

*This catalog is auto-generated. Do not edit manually.*
