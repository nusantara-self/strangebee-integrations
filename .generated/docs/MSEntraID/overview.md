# MSEntraID


## Subscription Information

- **Registration Required:** Yes
- **Subscription Required:** Yes
- **Free Subscription Available:** No

## Analyzers (4)

### MSEntraID_GetDirectoryAuditLogs `v1.0`
Pull Microsoft Entra ID directory audit logs for a user within the specified timeframe.

- **Data Types:** `mail`
- **Configuration:** [.upstream/cortex/analyzers/MSEntraID/MSEntraID_GetDirectoryAuditLogs.json](.upstream/cortex/analyzers/MSEntraID/MSEntraID_GetDirectoryAuditLogs.json)

### MSEntraID_GetUserInfo `v1.0`
Get information about the user from Microsoft Entra ID, using the mail

- **Data Types:** `mail`
- **Configuration:** [.upstream/cortex/analyzers/MSEntraID/MSEntraID_GetUserInfo.json](.upstream/cortex/analyzers/MSEntraID/MSEntraID_GetUserInfo.json)

### MSEntraID_GetSignIns `v1.0`
Pull all Microsoft Entra ID sign ins for a user within the specified amount of time.

- **Data Types:** `mail`
- **Configuration:** [.upstream/cortex/analyzers/MSEntraID/MSEntraID_GetSignIns.json](.upstream/cortex/analyzers/MSEntraID/MSEntraID_GetSignIns.json)

### MSEntraID_GetManagedDevicesInfo `v1.0`
Get Microsoft Intune Managed Device(s) Details from hostname or mail

- **Data Types:** `mail`, `hostname`
- **Configuration:** [.upstream/cortex/analyzers/MSEntraID/MSEntraID_GetManagedDevicesInfo.json](.upstream/cortex/analyzers/MSEntraID/MSEntraID_GetManagedDevicesInfo.json)

---

## Responders (5)

### MSEntraID_enableUser `v1.0`
Enable user in Microsoft Entra ID for a User Principal Name. (mail)

- **Data Types:** `thehive:case_artifact`
- **Configuration:** [.upstream/cortex/responders/MSEntraID/MSEntraID_enableUser.json](.upstream/cortex/responders/MSEntraID/MSEntraID_enableUser.json)

### MSEntraID_revokeSignInSessions `v1.1`
Invalidates all the refresh tokens issued to applications for a Microsoft Entra ID user (as well as session cookies in a user's browser)

- **Data Types:** `thehive:case_artifact`
- **Configuration:** [.upstream/cortex/responders/MSEntraID/MSEntraID_revokeSignInSessions.json](.upstream/cortex/responders/MSEntraID/MSEntraID_revokeSignInSessions.json)

### MSEntraID_disableUser `v1.0`
Disable user in Microsoft Entra ID for a User Principal Name. (mail)

- **Data Types:** `thehive:case_artifact`
- **Configuration:** [.upstream/cortex/responders/MSEntraID/MSEntraID_disableUser.json](.upstream/cortex/responders/MSEntraID/MSEntraID_disableUser.json)

### MSEntraID_ForcePasswordResetWithMFA `v1.0`
Force password reset at next login with MFA verification before password change for a User Principal Name. (mail)

- **Data Types:** `thehive:case_artifact`
- **Configuration:** [.upstream/cortex/responders/MSEntraID/MSEntraID_ForcePasswordResetWithMFA.json](.upstream/cortex/responders/MSEntraID/MSEntraID_ForcePasswordResetWithMFA.json)

### MSEntraID_ForcePasswordReset `v1.0`
Force password reset at next login for a User Principal Name. (mail)

- **Data Types:** `thehive:case_artifact`
- **Configuration:** [.upstream/cortex/responders/MSEntraID/MSEntraID_ForcePasswordReset.json](.upstream/cortex/responders/MSEntraID/MSEntraID_ForcePasswordReset.json)

---

## Statistics

- **Total Analyzers:** 4
- **Total Responders:** 5
- **Total Functions:** 0
- **Total Integrations:** 9

---

*This file is auto-generated from the integration manifest. Do not edit manually.*
