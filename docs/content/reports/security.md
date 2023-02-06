---
title: "Security report"
date: 2020-06-24T21:16:10+03:00
weight: 1
draft: false
description: "Provides actionable recommendations and insight into an attacker's view of your network"
---

{{% notice info %}}
Check out [the documentation for other reports available in the Infection Monkey]({{< ref "/reports" >}}).
{{% /notice %}}

The Infection Monkey's **Security Report** provides you with actionable recommendations and insight into an attacker's view of your network. You can download a PDF of an example report here:

{{%attachments title="Download the PDF" pattern=".*(pdf)"/%}}

The report is split into three main categories:

- [Overview](#overview)
  - [High-level information](#high-level-information)
  - [Used credentials](#used-credentials)
  - [Exploits and targets](#exploits-and-targets)
  - [Security findings](#security-findings)
- [Recommendations](#recommendations)
  - [Machine-related recommendations relating to specific CVEs](#machine-related-recommendations-relating-to-specific-cves)
  - [Machine-related recommendations relating to network security and segmentation](#machine-related-recommendations-relating-to-network-security-and-segmentation)
- [The network from the Monkey's eyes](#the-network-from-the-monkeys-eyes)
  - [Network infection map](#network-infection-map)
  - [Scanned servers](#scanned-servers)
  - [Stolen credentials](#stolen-credentials)

## Overview

The overview section of the report provides high-level information about the Infection Monkey's execution and main security findings.

### High-level information

This section shows general information about the Infection Monkey's execution, including which machine the infection originated from and how long the breach simulation took.

![Overview](/images/usage/reports/sec_report_1_overview.png "Overview")

### Used credentials

This section shows which credentials were used for brute-forcing.

![Used Credentials](/images/usage/reports/sec_report_2_users_passwords.png "Used Credentials")

### Exploits and targets

This section shows which exploits were attempted in this simulation and which targets the Infection Monkey scanned and tried to exploit.

![Exploits and Targets](/images/usage/reports/sec_report_3_exploits_ips.png "Exploits and Targets")

### Security findings

This section highlights the most important security threats and issues discovered during the attack.

![Threats and issues](/images/usage/reports/sec_report_4_threats_and_issues.png "Threats and issues")

## Recommendations

This section contains recommendations for improving your security, including actionable mitigation steps.

### Machine-related recommendations relating to specific CVEs

![Machine-related recommendations](/images/usage/reports/sec_report_5_machine_related.png "Machine related recommendations")

### Machine-related recommendations relating to network security and segmentation

![Machine-related recommendations](/images/usage/reports/sec_report_6_machine_related_network.png "Machine related recommendations")

## The network from the Monkey's eyes

This section contains tables that summarize what Infection Monkey found.

### Scanned servers

This section shows the attack surface the Infection Monkey discovered.

![Scanned servers](/images/usage/reports/sec_report_8_network_services.png "Scanned servers")

### Stolen credentials

This section shows which credentials the Infection Monkey was able to steal from breached machines during this simulation.

![Stolen creds](/images/usage/reports/sec_report_10_stolen_credentials.png "Stolen creds")
