---
title: "AWS Security Hub integration"
date: 2020-06-28T10:38:12+03:00
draft: false
description: "Correlate the Monkey's findings with the native security solutions and benchmark scores."
tags: ["aws", "integration"]
---

The Infection Monkey integration with the [AWS Security Hub](https://docs.aws.amazon.com/securityhub/latest/userguide/what-is-securityhub.html) allows anyone to verify and test the resilience of their AWS environment and correlate this information with the native security solutions and benchmark score.

![AWS security hub logo](/images/usage/integrations/AWS-Security-Hub-logo.png "AWS security hub logo")

The integration will send all Infection Monkey findings (typically 10 to 40) to the AWS Security Hub at the end of a breach simulation.

## Setup

If the correct AWS IAM role permissions have been set on the Monkey Island machine, it will automatically export its findings to the AWS Security Hub.

### Specific permissions required for the AWS Security Hub

- `"securityhub:UpdateFindings"`
- `"securityhub:BatchImportFindings"`


Note that this integration is specifically between your Monkey Island and the AWS Security Hub. The Infection Monkey is a free project, and there is no centralized infrastructure.

### Enabling finding reception

Before starting the scan, make sure that the AWS Security Hub is accepting findings by enabling the Infection Monkey integration. Find **GuardiCore: AWS Infection Monkey** integration on the list and click on **Accept findings**.

![Enabled integration](/images/usage/integrations/security-hub-enable-accepting-findings.png "Enabled integration")

## Integration details

The Infection Monkey reports the following types of issues to the AWS Security Hub: `Software and Configuration Checks/Vulnerabilities/CVE`.

Specifically, the Infection Monkey sends findings for all vulnerabilities it finds along with generic findings on the network (such as segmentation issues). Our normalized severity is 100, while most issues we report range between one and 10.

## Regions

The Infection Monkey is usable on all public AWS instances.

## Example

After setting up the Infection Monkey in AWS and attaching the correct IAM roles to your Monkey Island machine, the report findings were exported to the AWS Security Hub.

1. Navigate to `Findings`.
2. Click on a specific finding to see more details and possible solutions.

![AWS Security hub console example](/images/usage/integrations/security-hub-console-example.png "AWS Security hub console example")
