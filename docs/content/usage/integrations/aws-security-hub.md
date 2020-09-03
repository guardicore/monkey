---
title: "AWS Security Hub integration"
date: 2020-06-28T10:38:12+03:00
draft: false
description: "Correlate the Monkey's findings with the native security solutions and benchmark scores."
tags: ["aws", "integration"]
---

The Infection Monkey integration with the [AWS Security Hub](https://docs.aws.amazon.com/securityhub/latest/userguide/what-is-securityhub.html) allows anyone to verify and test the resilience of their AWS environment and correlate this information with the native security solutions and benchmark score.

![AWS security hub logo](/images/usage/integrations/AWS-Security-Hub-logo.png "AWS security hub logo")

The integration will send _all_ Infection Monkey findings (typically low tens of findings) to the security hub at the end of a Monkey breach simulation.

## Setup

If the correct permissions have been set on the AWS IAM role of the Monkey Island machine, then the Island will automatically export its findings to the AWS security hub.

### Specific permissions required for security hub

- `"securityhub:UpdateFindings"`
- `"securityhub:BatchImportFindings"`

Note that the integration is specifically between your Monkey Island and the security hub. The Infection Monkey is an free project and there is no centralised infrastructure.

## Integration details

The Infection Monkey reports the following types of issues to the AWS security hub: `Software and Configuration Checks/Vulnerabilities/CVE`.

Specifically, the Island sends findings for all vulnerabilities it finds along with generic findings on the network (such as segmentation issues). Our normalized severity is 100, while most issues we report range between 1 and 10.

## Regions

The Infection Monkey is usable on all public AWS instances.

## Example

After setting up a monkey environment in AWS and attaching the correct IAM roles to the monkey island machine, the report findings were exported to the security hub.

1. Navigate to `Findings`.
2. Press on a specific finding to see more details and possible solutions.

![AWS Security hub console example](/images/usage/integrations/security-hub-console-example.png "AWS Security hub console example")
