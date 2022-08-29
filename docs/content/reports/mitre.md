---
title: "MITRE ATT&CK report"
description: "Maps the Monkey's actions to the MITRE ATT&CK knowledge base"
date: 2020-06-24T21:17:18+03:00
weight: 3
draft: false
---

{{% notice info %}}
Check out [the documentation for other reports available in the Infection Monkey]({{< ref "/reports" >}}) and [the documentation for supported ATT&CK techniques]({{< ref "/reference/mitre_techniques" >}}).
{{% /notice %}}

The Infection Monkey maps its actions to the [MITRE ATT&CK](https://attack.mitre.org/) knowledge base. After simulating an advanced persistent threat (APT) attack, it generates a report summarizing the success of the techniques utilized along with recommended mitigation steps, helping you identify and mitigate attack paths in your environment.

Watch the overview video:

{{% youtube 3tNrlutqazQ %}}

## How to use the report

The MITRE ATT&CK report is centered around the ATT&CK matrix:

![MITRE Report](/images/usage/reports/mitre-report-0.png "MITRE Report")

The Infection Monkey rates your network on the attack techniques it attempted, assigning one of the corresponding labels to each:

- {{< label danger Red >}}: The Infection Monkey **successfully used** this technique in the simulation. This means your network is vulnerable to the technique.
- {{< label warning Yellow >}}: The Infection Monkey **tried to use** the technique, but wasn’t successful. This means your network isn't vulnerable to the way Infection Monkey employed this technique.
- {{< label unused "Dark Gray" >}}: The Monkey **didn't try** the technique. Perhaps it wasn't relevant to this network.
- {{< label disabled "Light Gray" >}}: The Monkey **didn't try** the technique since it wasn't configured.

By clicking on each of the listed techniques, you can see exactly how the Infection Monkey used it and any recommended mitigation steps. For example, let's look at the [**Brute Force**](https://attack.mitre.org/techniques/T1110/) technique that's a part of employing the [**Credentials Access**](https://attack.mitre.org/tactics/TA0006/) tactic:

![MITRE Report Credentials Access technique](/images/usage/reports/mitre-report-cred-access.png "MITRE Report Credentials Access technique")

In this example, you can see how the Infection Monkey was able to use an old `root` password to access all machines in the network. When scrolling to the bottom of this list, you can also see the mitigation steps recommended, including reconfiguring your **Account Use Policies** and implementing **Multi-factor Authentication**.

![MITRE Report Credentials Access technique](/images/usage/reports/mitre-report-cred-access-mitigations.png "MITRE Report Credentials Access technique")
