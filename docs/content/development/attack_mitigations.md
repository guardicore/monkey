---
title: "MITRE ATT&CK Mitigations"
date: 2021-09-30T08:18:37+03:00
draft: true
weight: 10
---

{{% notice info %}}
Check out [the documentation for the MITRE ATT&CK techniques as well]({{< ref "/reports/mitre" >}}).
{{% /notice %}}

## Summary

Attack Mitigations are presented in MITRE ATT&CK report. They appear next to
descriptions of attack techniques and suggest steps that can be taken to reduce
the risk of that particular technique being successful in a network. They also
provide links for further reading on https://attack.mitre.org/

The Infection Monkey is shipped with pre-processed information about MITRE
ATT&CK mitigations located at
`monkey/monkey_island/cc/setup/mongo/attack_mitigations.json`. This may need to
be periodically updated as the MITRE ATT&CK framework evolves.


## Updating the MITRE ATT&CK mitigations data
1. Clone the [MITRE Cyber Threat Intelligence
   Repository](https://github.com/mitre/cti) or the [Guardicore
   fork](https://github.com/guardicore/cti):
   ```
   $ CTI_REPO=$PWD/cti
   $ git clone <REPO> $CTI_REPO
   ```
2. Start a MongoDB v4.2 server.
3. Run the script to generate the `attack_mitigations.json` file:
   ```
   $ cd monkey/deployment_scripts/dump_attack_mitigations
   $ pip install -r requirements.txt
   $ python dump_attack_mitigations.py --cti-repo $CTI_REPO --dump-file-path ../../monkey/monkey_island/cc/setup/mongo/attack_mitigations.json
   ```
