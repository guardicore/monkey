---
title: "ATT&CK   Mitigations"
date: 2021-09-30T08:18:37+03:00
draft: true
pre: '&nbsp<b><u>!!</u></b> '
weight: 10
---

{{% notice info %}}
Check out [the documentation for the MITRE ATT&CK techniques as well]({{< ref "/reports/mitre" >}}).
{{% /notice %}}

Infection Monkey is shipped with pre-existing ATT&CK mitigations located at `monkey/monkey_island/cc/setup/mongo/attack_mitigations.json`.
This allows Monkey Island to be setup faster.

The `attack_mitigations.json` can be updated by running `monkey/deployment_scripts/dump_attack_mitigations.py` by providing the link to
[Cyber Threat Intelligence Repository](https://github.com/mitre/cti) , mongo host and port information and the dump file location.

When starting Monkey Island this information is stored in the mongo database almost instantly, making the setup faster.
