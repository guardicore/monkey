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

The report is split into the following categories:

- [Overview](#overview)
- [Segmentation Issues](#segmentation-issues)
- [Machine-related Recommendations](#machine-related-recommendations)
- [The Network from Infection Monkey's Eyes](#the-network-from-infection-monkeys-eyes)

## Overview

The Overview section of the report provides high-level information about the Infection Monkey's
execution, including the machines from which the infection originated, how long the breach
simulation took, and the configuration of the Agents.

![Overview](/images/usage/reports/sec_report_1_overview.png "Overview")

![Used Credentials](/images/usage/reports/sec_report_2_users_passwords.png "Used Credentials")

## Segmentation Issues

This section reports the segmentation issues in your network.

TODO: Add screenshot!

## Machine-related Recommendations

Here, you will find recommendations for improving your network's
security, including actionable mitigation steps.

![Machine-related recommendations](/images/usage/reports/sec_report_5_machine_related.png "Machine related recommendations")

![Machine-related recommendations](/images/usage/reports/sec_report_6_machine_related_network.png "Machine related recommendations")

## The Network from Infection Monkey's Eyes

This section contains a summary of what Infection Monkey found, including
details of scanned servers, breached servers, and stolen credentials.

![Scanned servers](/images/usage/reports/sec_report_8_network_services.png "Scanned servers")

![Stolen creds](/images/usage/reports/sec_report_10_stolen_credentials.png "Stolen creds")
