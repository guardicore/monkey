---
title: "MITRE ATT&CK report"
date: 2020-06-24T21:17:18+03:00
draft: false
---

The Monkey maps its actions to the [MITRE ATT&CK](https://attack.mitre.org/) knowledge base: It provides a new report with the utilized techniques and recommended mitigations, to help you simulate an APT attack on your network and mitigate real attack paths intelligently.

Watch an overview video:

{{% youtube 3tNrlutqazQ %}}

## How to use the report

The MITRE ATT&CK report is centred around the ATT&CK matrix:

![MITRE Report](/images/usage/reports/mitre-report-0.jpg "MITRE Report")

The Monkey rates your network on the attack techniques it attempted. For each technique, you can get

- **Red**: The Monkey **successfully used** the technique in the simulation. That means your network is vulnerable to this technique being employed.
- **Yellow**: The Monkey **tried to use** the technique, but didn’t manage to. That means your network isn’t vulnerable to the way Monkey employs this technique.

Then, you can see exactly HOW the technique was used in this attack, and also what you should do to mitigate it, by clicking on the technique and seeing the details. For example, let’s look at the “Private keys” technique that’s a part of employing the “Credentials Access” tactic:

![MITRE Report Credentials Access technique](/images/usage/reports/mitre-report-cred-access.jpg "MITRE Report Credentials Access technique")

In this example, you can see **from which machines** the Monkey was able to steal SSH keys, and the mitigations recommended, including **Restricting File and Directory access** and implementing **Network Segmentation**.
