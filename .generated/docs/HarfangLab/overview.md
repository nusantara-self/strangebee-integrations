# HarfangLab


## Subscription Information

- **Subscription Required:** Yes
- **Free Subscription Available:** No

## Responders (31)

### HarfangLab-GetArtifactUSN `v1.0`
Get USN logs artifact

- **Data Types:** `thehive:case`
- **Configuration:** [.upstream/cortex/responders/HarfangLab/HarfangLab_GetArtifactUSN.json](.upstream/cortex/responders/HarfangLab/HarfangLab_GetArtifactUSN.json)

### HarfangLab-IsolateHost `v1.0`
Isolate machine with HarfangLab EDR

- **Data Types:** `thehive:case`, `thehive:alert`
- **Configuration:** [.upstream/cortex/responders/HarfangLab/HarfangLab_Isolate.json](.upstream/cortex/responders/HarfangLab/HarfangLab_Isolate.json)

### HarfangLab-KillProcess `v1.0`
Kill a process

- **Data Types:** `thehive:case`, `thehive:alert`
- **Configuration:** [.upstream/cortex/responders/HarfangLab/HarfangLab_KillProcess.json](.upstream/cortex/responders/HarfangLab/HarfangLab_KillProcess.json)

### HarfangLab-GetScheduledTasks `v1.0`
Get scheduled tasks on a host

- **Data Types:** `thehive:case`
- **Configuration:** [.upstream/cortex/responders/HarfangLab/HarfangLab_GetScheduledTasks.json](.upstream/cortex/responders/HarfangLab/HarfangLab_GetScheduledTasks.json)

### HarfangLab-GetArtifactMFT `v1.0`
Get MFT artifact

- **Data Types:** `thehive:case`
- **Configuration:** [.upstream/cortex/responders/HarfangLab/HarfangLab_GetArtifactMFT.json](.upstream/cortex/responders/HarfangLab/HarfangLab_GetArtifactMFT.json)

### HarfangLab-GetArtifactEvtx `v1.0`
Get Windows event logs artifact

- **Data Types:** `thehive:case`
- **Configuration:** [.upstream/cortex/responders/HarfangLab/HarfangLab_GetArtifactEvtx.json](.upstream/cortex/responders/HarfangLab/HarfangLab_GetArtifactEvtx.json)

### HarfangLab-DumpProcess `v1.0`
Dump process memory

- **Data Types:** `thehive:case`
- **Configuration:** [.upstream/cortex/responders/HarfangLab/HarfangLab_DumpProcess.json](.upstream/cortex/responders/HarfangLab/HarfangLab_DumpProcess.json)

### HarfangLab-GetSessions `v1.0`
Get sessions on a host

- **Data Types:** `thehive:case`
- **Configuration:** [.upstream/cortex/responders/HarfangLab/HarfangLab_GetSessions.json](.upstream/cortex/responders/HarfangLab/HarfangLab_GetSessions.json)

### HarfangLab-GetDrivers `v1.0`
Get drivers loaded on a host

- **Data Types:** `thehive:case`
- **Configuration:** [.upstream/cortex/responders/HarfangLab/HarfangLab_GetDrivers.json](.upstream/cortex/responders/HarfangLab/HarfangLab_GetDrivers.json)

### HarfangLab-GetRunKeys `v1.0`
Get RUN keys on a host

- **Data Types:** `thehive:case`
- **Configuration:** [.upstream/cortex/responders/HarfangLab/HarfangLab_GetRunKeys.json](.upstream/cortex/responders/HarfangLab/HarfangLab_GetRunKeys.json)

### HarfangLab-GetNetworkShares `v1.0`
Get network shares on a host

- **Data Types:** `thehive:case`
- **Configuration:** [.upstream/cortex/responders/HarfangLab/HarfangLab_GetNetworkShares.json](.upstream/cortex/responders/HarfangLab/HarfangLab_GetNetworkShares.json)

### HarfangLab-GetArtifactLogs `v1.0`
Get Linux logs artifact

- **Data Types:** `thehive:case`
- **Configuration:** [.upstream/cortex/responders/HarfangLab/HarfangLab_GetArtifactLogs.json](.upstream/cortex/responders/HarfangLab/HarfangLab_GetArtifactLogs.json)

### HarfangLab-SearchDestinationIP `v1.0`
Search an IP in HarfangLab EDR's telemetry

- **Data Types:** `thehive:case_artifact`
- **Configuration:** [.upstream/cortex/responders/HarfangLab/HarfangLab_SearchDestinationIP.json](.upstream/cortex/responders/HarfangLab/HarfangLab_SearchDestinationIP.json)

### HarfangLab_SearchDriverByHash `v1.0`
Search a driver load in HarfangLab EDR's telemetry per hash

- **Data Types:** `thehive:case_artifact`
- **Configuration:** [.upstream/cortex/responders/HarfangLab/HarfangLab_SearchDriverByHash.json](.upstream/cortex/responders/HarfangLab/HarfangLab_SearchDriverByHash.json)

### HarfangLab-GetPipes `v1.0`
Get pipes on a host

- **Data Types:** `thehive:case`
- **Configuration:** [.upstream/cortex/responders/HarfangLab/HarfangLab_GetPipes.json](.upstream/cortex/responders/HarfangLab/HarfangLab_GetPipes.json)

### HarfangLab_SearchDriverByFileName `v1.0`
Search a driver load in HarfangLab EDR's telemetry per filename

- **Data Types:** `thehive:case_artifact`
- **Configuration:** [.upstream/cortex/responders/HarfangLab/HarfangLab_SearchDriverByFileName.json](.upstream/cortex/responders/HarfangLab/HarfangLab_SearchDriverByFileName.json)

### HarfangLab-SearchSourceIP `v1.0`
Search an IP in HarfangLab EDR's telemetry

- **Data Types:** `thehive:case_artifact`
- **Configuration:** [.upstream/cortex/responders/HarfangLab/HarfangLab_SearchSourceIP.json](.upstream/cortex/responders/HarfangLab/HarfangLab_SearchSourceIP.json)

### HarfangLab-GetBinary `v1.0`
Get binary information and download link

- **Data Types:** `thehive:case_artifact`
- **Configuration:** [.upstream/cortex/responders/HarfangLab/HarfangLab_GetBinary.json](.upstream/cortex/responders/HarfangLab/HarfangLab_GetBinary.json)

### HarfangLab-GetProcesses `v1.0`
Get processes running on a host

- **Data Types:** `thehive:case`
- **Configuration:** [.upstream/cortex/responders/HarfangLab/HarfangLab_GetProcesses.json](.upstream/cortex/responders/HarfangLab/HarfangLab_GetProcesses.json)

### HarfangLab-GetWMI `v1.0`
Get WMI items on a host

- **Data Types:** `thehive:case`
- **Configuration:** [.upstream/cortex/responders/HarfangLab/HarfangLab_GetWMI.json](.upstream/cortex/responders/HarfangLab/HarfangLab_GetWMI.json)

### HarfangLab-GetPrefetches `v1.0`
Get prefetches on a host

- **Data Types:** `thehive:case`
- **Configuration:** [.upstream/cortex/responders/HarfangLab/HarfangLab_GetPrefetches.json](.upstream/cortex/responders/HarfangLab/HarfangLab_GetPrefetches.json)

### HarfangLab-GetPersistence `v1.0`
Get persistence items on a Linux host

- **Data Types:** `thehive:case`
- **Configuration:** [.upstream/cortex/responders/HarfangLab/HarfangLab_GetPersistence.json](.upstream/cortex/responders/HarfangLab/HarfangLab_GetPersistence.json)

### HarfangLab-GetArtifactRamdump `v1.0`
Get RAM dump artifact

- **Data Types:** `thehive:case`
- **Configuration:** [.upstream/cortex/responders/HarfangLab/HarfangLab_GetArtifactRamdump.json](.upstream/cortex/responders/HarfangLab/HarfangLab_GetArtifactRamdump.json)

### HarfangLab-GetArtifactAll `v1.0`
Get all artifacts

- **Data Types:** `thehive:case`
- **Configuration:** [.upstream/cortex/responders/HarfangLab/HarfangLab_GetArtifactAll.json](.upstream/cortex/responders/HarfangLab/HarfangLab_GetArtifactAll.json)

### HarfangLab-UnisolateHost `v1.0`
Isolate machine with HarfangLab EDR

- **Data Types:** `thehive:case`, `thehive:alert`
- **Configuration:** [.upstream/cortex/responders/HarfangLab/HarfangLab_Unisolate.json](.upstream/cortex/responders/HarfangLab/HarfangLab_Unisolate.json)

### HarfangLab-GetArtifactPrefetch `v1.0`
Get prefetches artifact

- **Data Types:** `thehive:case`
- **Configuration:** [.upstream/cortex/responders/HarfangLab/HarfangLab_GetArtifactPrefetch.json](.upstream/cortex/responders/HarfangLab/HarfangLab_GetArtifactPrefetch.json)

### HarfangLab-GetArtifactFilesystem `v1.0`
Get Linux filesystem artifact

- **Data Types:** `thehive:case`
- **Configuration:** [.upstream/cortex/responders/HarfangLab/HarfangLab_GetArtifactFilesystem.json](.upstream/cortex/responders/HarfangLab/HarfangLab_GetArtifactFilesystem.json)

### HarfangLab-GetArtifactHives `v1.0`
Get Hives artifact

- **Data Types:** `thehive:case`
- **Configuration:** [.upstream/cortex/responders/HarfangLab/HarfangLab_GetArtifactHives.json](.upstream/cortex/responders/HarfangLab/HarfangLab_GetArtifactHives.json)

### HarfangLab-GetStartupFiles `v1.0`
Get startup files on a host

- **Data Types:** `thehive:case`
- **Configuration:** [.upstream/cortex/responders/HarfangLab/HarfangLab_GetStartupFiles.json](.upstream/cortex/responders/HarfangLab/HarfangLab_GetStartupFiles.json)

### HarfangLab-GetServices `v1.0`
Get services on a host

- **Data Types:** `thehive:case`
- **Configuration:** [.upstream/cortex/responders/HarfangLab/HarfangLab_GetServices.json](.upstream/cortex/responders/HarfangLab/HarfangLab_GetServices.json)

### HarfangLab-SearchHash `v1.0`
Search a hash in HarfangLab EDR's telemetry

- **Data Types:** `thehive:case_artifact`
- **Configuration:** [.upstream/cortex/responders/HarfangLab/HarfangLab_SearchHash.json](.upstream/cortex/responders/HarfangLab/HarfangLab_SearchHash.json)

---

## Statistics

- **Total Analyzers:** 0
- **Total Responders:** 31
- **Total Functions:** 0
- **Total Integrations:** 31

---

*This file is auto-generated from the integration manifest. Do not edit manually.*
