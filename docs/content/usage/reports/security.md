---
title: "Security report"
date: 2020-06-24T21:16:10+03:00
draft: false
---

{{% notice info %}}
Check out [the documentation for the other reports as well](../).
{{% /notice %}}

The Monkey's Security Report is built to provide you with actionable recommendations and insight to the Attacker's view of your network. You can download a PDF of this example report:

{{%attachments title="Download the PDF" pattern=".*(pdf)"/%}}

The report is split into 3 main categories: "Overview", "Recommendations" and "The network from the Monkey's eyes".

- [Overview](#overview)
  - [High level information](#high-level-information)
  - [Used Credentials](#used-credentials)
  - [Exploits and targets](#exploits-and-targets)
  - [Security Findings](#security-findings)
- [Recommendations](#recommendations)
  - [Machine related recommendations relating to specific CVEs](#machine-related-recommendations-relating-to-specific-cves)
  - [Machine related recommendations relating to network security and segmentation](#machine-related-recommendations-relating-to-network-security-and-segmentation)
- [The network from the Monkey's eyes](#the-network-from-the-monkeys-eyes)
  - [Network infection map](#network-infection-map)
  - [Scanned servers](#scanned-servers)
  - [Exploits and post-breach actions](#exploits-and-post-breach-actions)
  - [Stolen Credentials](#stolen-credentials)

## Overview

The overview section of the report provides high-level information about the Monkey execution and the main security findings that the Monkey has found.

### High level information

The report starts with information about the execution, including how long the simulation took and from which machine the infection started from.

![Overview](/images/usage/reports/sec_report_1_overview.png "Overview")

### Used Credentials

The report will show which credentials were used for brute-forcing.

![Used Credentials](/images/usage/reports/sec_report_2_users_passwords.png "Used Credentials")

### Exploits and targets

The report shows which exploits were attempted in this simulation and which targets the Monkey scanned and tried to exploit.

![Exploits and Targets](/images/usage/reports/sec_report_3_exploits_ips.png "Exploits and Targets")

### Security Findings

The report highlights the most important security threats and issues the Monkey discovered during the attack.

![Threats and issues](/images/usage/reports/sec_report_4_threats_and_issues.png "Threats and issues")

## Recommendations

This section contains the Monkey's recommendations for improving your security - what mitigations you need to implement.

### Machine related recommendations relating to specific CVEs

![Machine related recommendations](/images/usage/reports/sec_report_5_machine_related.png "Machine related recommendations")

### Machine related recommendations relating to network security and segmentation

![Machine related recommendations](/images/usage/reports/sec_report_6_machine_related_network.png "Machine related recommendations")

## The network from the Monkey's eyes

This section contains the Infection Map and some summary tables on servers the Monkey has found.

### Network infection map

This part shows the network map and a breakdown of how many machines were breached.

![Network map](/images/usage/reports/sec_report_7_network_map.png "Network map")

### Scanned servers

This part shows the attack surface the Monkey has found.

![Scanned servers](/images/usage/reports/sec_report_8_network_services.png "Scanned servers")

### Exploits and post-breach actions

This part shows which exploits and Post Breach Actions the Monkey has performed in this simulation.

![Exploits and PBAs](/images/usage/reports/sec_report_9_exploits_pbas.png "Exploits and PBAs")

### Stolen Credentials

This part shows which credentials the Monkey was able to steal from breached machines in this simulation.

![Stolen creds](/images/usage/reports/sec_report_10_stolen_credentials.png "Stolen creds")
