# Duo_Security


## Responders (3)

### DuoUnlockUserAccount `v1.0`
Unlock User Account in Duo Security via AdminAPI (The user must complete secondary authentication)

- **Data Types:** `thehive:case_artifact`
- **Configuration:** [.upstream/cortex/responders/Duo_Security/DuoUnlockUserAccount.json](.upstream/cortex/responders/Duo_Security/DuoUnlockUserAccount.json)

### DuoBypassUserAccount `v1.0`
Put User Account into Bypass mode in Duo Security via AdminAPI (The user will not be prompted when logging in.)

- **Data Types:** `thehive:case_artifact`
- **Configuration:** [.upstream/cortex/responders/Duo_Security/DuoBypassUserAccount.json](.upstream/cortex/responders/Duo_Security/DuoBypassUserAccount.json)

### DuoLockUserAccount `v1.0`
Lock User Account in Duo Security via AdminAPI (The user will not be able to log in)

- **Data Types:** `thehive:case_artifact`
- **Configuration:** [.upstream/cortex/responders/Duo_Security/DuoLockUserAccount.json](.upstream/cortex/responders/Duo_Security/DuoLockUserAccount.json)

---

## Statistics

- **Total Analyzers:** 0
- **Total Responders:** 3
- **Total Functions:** 0
- **Total Integrations:** 3

---

*This file is auto-generated from the integration manifest. Do not edit manually.*
