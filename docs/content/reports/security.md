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

The Infection Monkey's **Security Report** provides you with actionable recommendations and insight into an attacker's view of your network.

The report is split into the following categories:

- [Overview](#overview)
- [Segmentation Issues](#segmentation-issues)
- [Machine-related Recommendations](#machine-related-recommendations)
- [The Network from Infection Monkey's Eyes](#the-network-from-infection-monkeys-eyes)

## Overview

The Overview section of the report provides high-level information about the Infection Monkey's
execution, including the machines from which the infection originated, how long the breach
simulation took, and the configuration of the Agents.

![Overview](/images/island/reports_page/security_report_overview.png "Overview")

## Segmentation Issues

This section reports the segmentation issues in your network.

![Segmentation Issues](/images/island/reports_page/security_report_segmentation_issues.png "Segmentation Issues")

## Machine-related Recommendations

Here, you will find recommendations for improving your network's
security, including actionable mitigation steps.

![Machine-related Recommendations](/images/island/reports_page/security_report_machine_related_recommendations.png "Machine-related Recommendations")


## The Network from Infection Monkey's Eyes

This section contains a summary of what Infection Monkey found, including
details of scanned servers, breached servers, and stolen credentials.

![The Network from Infection Monkey's Eyes](/images/island/reports_page/security_report_network_from_monkeys_eyes.png "The Network from Infection Monkey's Eyes")
