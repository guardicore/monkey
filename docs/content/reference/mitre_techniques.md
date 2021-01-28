---
title: "MITRE ATT&CK"
date: 2020-09-24T08:18:37+03:00
draft: false
pre: '&nbsp<b><u>&</u></b> '
weight: 10 
---

{{% notice info %}}
Check out [the documentation for the MITRE ATT&CK report as well](../../usage/reports/mitre).
{{% /notice %}}

The Monkey maps its actions to the [MITRE ATT&CK](https://attack.mitre.org/) knowledge base and based on this,
 provides a report detailing the techniques it used and recommended mitigations.
 The idea is to help you simulate an APT attack on your network and mitigate real attack paths intelligently.
 
 In the following table we provide the list of all the ATT&CK techniques the Monkey provides info about,
 categorized by tactic. You can follow any of the links to learn more about a specific technique or tactic.


| TACTIC                                                            | TECHNIQUES                                                                                 |
|---                                                                |---                                                                                         |
| [Execution](https://attack.mitre.org/tactics/TA0002/)             | [Command-line Interface](https://attack.mitre.org/techniques/T1059/)                       |
|                                                                   | [Execution Through Module Load](https://attack.mitre.org/techniques/T1129/)                |
|                                                                   | [Execution Through API](https://attack.mitre.org/techniques/T1106/)                        |
|                                                                   | [Powershell](https://attack.mitre.org/techniques/T1086/)                                   |
|                                                                   | [Scripting](https://attack.mitre.org/techniques/T1064/)                                    |
|                                                                   | [Service Execution](https://attack.mitre.org/techniques/T1035/)                            |
|                                                                   | [Trap](https://attack.mitre.org/techniques/T1154/)                                         |
| [Persistence](https://attack.mitre.org/tactics/TA0003/)           | [.bash_profile & .bashrc](https://attack.mitre.org/techniques/T1156/)                      |
|                                                                   | [Create Account](https://attack.mitre.org/techniques/T1136/)                               |
|                                                                   | [Hidden Files & Directories](https://attack.mitre.org/techniques/T1158/)                   |
|                                                                   | [Local Job Scheduling](https://attack.mitre.org/techniques/T1168/)                         |
|                                                                   | [Powershell Profile](https://attack.mitre.org/techniques/T1504/)                           |
|                                                                   | [Scheduled Task](https://attack.mitre.org/techniques/T1053/)                               |
|                                                                   | [Setuid & Setgid](https://attack.mitre.org/techniques/T1166/)                              |
| [Defence Evasion](https://attack.mitre.org/tactics/TA0005/)       | [BITS Job](https://attack.mitre.org/techniques/T1197/)                                     |
|                                                                   | [Clear Command History](https://attack.mitre.org/techniques/T1146/)                        |
|                                                                   | [File Deletion](https://attack.mitre.org/techniques/T1107/)                                |
|                                                                   | [File Permissions Modification](https://attack.mitre.org/techniques/T1222/)                |
|                                                                   | [Timestomping](https://attack.mitre.org/techniques/T1099/)                                 |
|                                                                   | [Signed Script Proxy Execution](https://attack.mitre.org/techniques/T1216/)                |
| [Credential Access](https://attack.mitre.org/tactics/TA0006/)     | [Brute Force](https://attack.mitre.org/techniques/T1110/)                                  |
|                                                                   | [Credential Dumping](https://attack.mitre.org/techniques/T1003/)                           |
|                                                                   | [Private Keys](https://attack.mitre.org/techniques/T1145/)                                 |
| [Discovery](https://attack.mitre.org/tactics/TA0007/)             | [Account Discovery](https://attack.mitre.org/techniques/T1087/)                            |
|                                                                   | [Remote System Discovery](https://attack.mitre.org/techniques/T1018/)                      |
|                                                                   | [System Information Discovery](https://attack.mitre.org/techniques/T1082/)                 |
|                                                                   | [System Network Configuration Discovery](https://attack.mitre.org/techniques/T1016/)       |
| [Lateral Movement](https://attack.mitre.org/tactics/TA0008/)      | [Exploitation Of Remote Services](https://attack.mitre.org/techniques/T1210/)              |
|                                                                   | [Pass The Hash](https://attack.mitre.org/techniques/T1075/)                                |
|                                                                   | [Remote File Copy](https://attack.mitre.org/techniques/T1105/)                             |
|                                                                   | [Remote Services](https://attack.mitre.org/techniques/T1021/)                              |
| [Collection](https://attack.mitre.org/tactics/TA0009/)            | [Data From Local System](https://attack.mitre.org/techniques/T1005)                        |
| [Command And Control](https://attack.mitre.org/tactics/TA0011/)   | [Connection Proxy](https://attack.mitre.org/techniques/T1090/)                             |
|                                                                   | [Uncommonly Used Port](https://attack.mitre.org/techniques/T1065/)                         |
|                                                                   | [Multi-hop Proxy](https://attack.mitre.org/techniques/T1188/)                              |
| [Exfiltration](https://attack.mitre.org/tactics/TA0010/)          | [Exfiltration Over Command And Control Channel](https://attack.mitre.org/techniques/T1041/)|
