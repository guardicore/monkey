---
title: "Ransomware report"
date: 2021-08-05T13:23:10+03:00
weight: 4
draft: false
description: "Provides information about ransomware simulation on your network"
---

{{% notice info %}}
Check out [the documentation for the Infection Monkey's ransomware
simulation]({{< ref "/usage/scenarios/ransomware-simulation" >}}) and [the
documentation for other reports available in the Infection Monkey]({{< ref
"/reports" >}}).
{{% /notice %}}

The Infection Monkey can be configured to [simulate a ransomware
attack](/usage/scenarios/ransomware-simulation) on your network. The
**Ransomware Report** provides you with insight into how ransomware might
behave within your environment.

The report is split into three sections:

- [Breach](#breach)
- [Lateral Movement](#lateral-movement)
- [Attack](#attack)

## Breach

The breach section shows when and where the ransomware infection began.

![Breach](/images/usage/reports/ransomware_report_1_breach.png "Breach")


## Lateral Movement

The lateral movement section provides information about how the simulated
ransomware was able to propagate through your network.


![Lateral
Movement](/images/usage/reports/ransomware_report_2_lateral_movement.png
"Lateral Movement")


## Attack

The attack section shows which files the simulated ransomware successfully
encrypted and the total number of files that were encrypted on your network.

![Attack](/images/usage/reports/ransomware_report_3_attack.png "Attack")
