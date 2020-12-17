---
title: "MITRE ATT&CK report"
date: 2020-06-24T21:17:18+03:00
draft: false
---

{{% notice info %}}
Check out [the documentation for the other reports](../) and [the documentation for supported ATT&CK techniques as well](../../../reference/mitre_techniques).
{{% /notice %}}

The Monkey maps its actions to the [MITRE ATT&CK](https://attack.mitre.org/) knowledge base: It provides a new report with the utilized techniques and recommended mitigations, to help you simulate an APT attack on your network and mitigate real attack paths intelligently.

Watch an overview video:

{{% youtube 3tNrlutqazQ %}}

## How to use the report

The MITRE ATT&CK report is centred around the ATT&CK matrix:

![MITRE Report](/images/usage/reports/mitre-report-0.png "MITRE Report")

The Monkey rates your network on the attack techniques it attempted. For each technique, you can get

- {{< label danger Red >}}: The Monkey **successfully used** the technique in the simulation. That means your network is vulnerable to this technique being employed.
- {{< label warning Yellow >}}: The Monkey **tried to use** the technique, but didn’t manage to. That means your network isn’t vulnerable to the way Monkey employs this technique.
- {{< label unused "Dark Gray" >}}: The Monkey **didn't try** the technique. Perhaps it wasn't relevant to this network.
- {{< label disabled "Light Gray" >}}: The Monkey **didn't try** the technique since it wasn't configured.

Then, you can see exactly HOW the technique was used in this attack, and also what you should do to mitigate it, by clicking on the technique and seeing the details. For example, let’s look at the [**Brute Force**](https://attack.mitre.org/techniques/T1110/) technique that’s a part of employing the [**Credentials Access**](https://attack.mitre.org/tactics/TA0006/) tactic:

![MITRE Report Credentials Access technique](/images/usage/reports/mitre-report-cred-access.png "MITRE Report Credentials Access technique")

In this example, you can see how the Monkey was able to use one old `root` password to access all machines in the network. When scrolling to the bottom of this list, you can also see the mitigation recommended, including **Account Use Policies** and implementing **Multiple Factor Authentication**.

![MITRE Report Credentials Access technique](/images/usage/reports/mitre-report-cred-access-mitigations.png "MITRE Report Credentials Access technique")
