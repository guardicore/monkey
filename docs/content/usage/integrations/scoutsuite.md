---
title: "Scoutsuite"
date: 2021-03-02T16:23:06+02:00
draft: false
weight: 10
---

### What is ScoutSuite?

<a href="https://github.com/nccgroup/ScoutSuite" target="_blank" >Scout Suite</a> is an open-source cloud security-auditing tool.
It queries the cloud API to gather configuration data of the cloud infrastructure. Based on configuration
data gathered ScoutSuite shows security issues and risks present in your infrastructure.

### Which cloud providers are supported?

So far the Infection Monkey only supports AWS.

### How to enable ScoutSuite?

First of all, Infection Monkey needs access to your cloud API. You can provide access
in the following ways:

 - Provide access keys:
    - Create a new user with ReadOnlyAccess and SecurityAudit policies and generate keys
    - Generate keys for your current user (faster but less secure)
 - Configure AWS CLI:
    - If the command-line interface is available on the Island, it will be used to access 
    the cloud API
    
More details about configuring ScoutSuite can be found in the tool itself, by choosing 
"Cloud Security Scan" in the "Run Monkey" options. 

After you're done with the setup, make sure that a checkmark appears next to the AWS option to 
verify that ScoutSuite can access the API.

![Successfull setup indicator](/images/usage/integrations/scoutsuite_aws_configured.png 
"Successful setup indicator")

### How to run cloud scan?

If you have successfully configured cloud scan, once the Monkey Agent is run **on the Island**, 
the cloud infrastructure will get scanned. To make this happen, you can simply click on "From Island" 
in the run options. The scope of network scan and other activities you configured the Agent to 
do are irrelevant for cloud security scan, except 
**Monkey Configuration -> System info collectors -> AWS collector** which needs to remain **enabled**.

### How to assess cloud scan results?

After the scan is done, ScoutSuite results will be sorted and applied to the ZeroTrust Extended framework 
and displayed as a part of the ZeroTrust report. The main difference between Infection Monkey findings and 
ScoutSuite findings is that ScoutSuite findings contain security rules. To see which rules were 
checked click on the "Rules" button next to the relevant test. You'll see a brief overview of the rules 
related to the test and a list of those rules. Expand a rule to see its description, remediation and 
more details about resources flagged. Each flagged resource has a path so you can easily locate 
them in the cloud and change the value that is deemed insecure.

![Open ScoutSuite rule](/images/usage/integrations/scoutsuite_report_rule.png 
"Successful setup indicator")
