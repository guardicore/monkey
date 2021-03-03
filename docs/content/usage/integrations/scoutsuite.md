---
title: "Scoutsuite"
date: 2021-03-02T16:23:06+02:00
draft: false
description: "Scout Suite is an open-source cloud security-auditing tool."
weight: 10
---

### About ScoutSuite

<a href="https://github.com/nccgroup/ScoutSuite" target="_blank" >Scout Suite</a> is an open-source cloud security-auditing tool.
It queries the cloud API to gather configuration data. Based on configuration
data gathered, ScoutSuite shows security issues and risks present in your infrastructure.

### Supported cloud providers

Currently, ScoutSuite integration only supports AWS environments.

### Enabling ScoutSuite

First, Infection Monkey needs access to your cloud API. You can provide access
in the following ways:

 - Provide access keys:
    - Create a new user with ReadOnlyAccess and SecurityAudit policies and generate keys
    - Generate keys for your current user (faster but less secure)
 - Configure AWS CLI:
    - If the command-line interface is available on the Island, it will be used to access 
    the cloud API
    
More details about configuring ScoutSuite can be found in the tool itself, by choosing 
"Cloud Security Scan" in the "Run Monkey" options. 

![Cloud scan option in run page](/images/usage/integrations/scoutsuite_run_page.png 
"Successful setup indicator")

After you're done with the setup, make sure that a checkmark appears next to the AWS option. This 
verifies that ScoutSuite can access the API.

![Successfull setup indicator](/images/usage/integrations/scoutsuite_aws_configured.png 
"Successful setup indicator")

### Running a cloud security scan

If you have successfully configured the cloud scan, Infection Monkey will scan
your cloud infrastructure when the Monkey Agent is run **on the Island**. You
can simply click on "From Island" in the run options to start the scan. The
scope of the network scan and other activities you may have configured the Agent
to perform are ignored by the ScoutSuite integration, except **Monkey
Configuration -> System info collectors -> AWS collector**, which needs to
remain **enabled**.


### Assessing scan results

After the scan is done, ScoutSuite results will be categorized according to the
ZeroTrust Extended framework and displayed as a part of the ZeroTrust report.
The main difference between Infection Monkey findings and ScoutSuite findings
is that ScoutSuite findings contain security rules. To see which rules were
checked, click on the "Rules" button next to the relevant test. You'll see a
list of rule dropdowns that are color coded according to their status. Expand a
rule to see its description, remediation and more details about resources
flagged. Each flagged resource has a path so you can easily locate it in the
cloud and remediate the issue.

![Open ScoutSuite rule](/images/usage/integrations/scoutsuite_report_rule.png 
"Successful setup indicator")
