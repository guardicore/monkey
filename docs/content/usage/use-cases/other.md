---
title: "Other"
date: 2020-08-12T13:07:55+03:00
draft: true
weight: 100
---

## Overview 

This page provides additional information about configuring monkeys, tips and tricks and creative usage scenarios.

## Tips and tricks

- Every network has its old “skeleton keys” that should have long been discarded. Configure the Monkey with old and stale passwords, but make sure that they were really discarded using the Monkey. To add the old passwords, in the island’s configuration, go to the “Exploit password list” under “Basic - Credentials” and use the “+” button to add the old passwords to the configuration. For example, here we added a few extra passwords (and a username as well) to the configuration:

![Exploit password and user lists](/images/usage/scenarios/user-password-lists.png "Exploit password and user lists")

- To see the Monkey executing in real-time on your servers, add the **post-breach action** command: `wall “Infection Monkey was here”`. This post breach command will broadcast a message across all open terminals on the servers the Monkey breached, to achieve the following: Let you know the Monkey ran successfully on the server. let you follow the breach “live” alongside the infection map, and check which terminals are logged and monitored inside your network. See below:

![How to configure post breach commands](/images/usage/scenarios/pba-example.png "How to configure post breach commands.")


## Assessing results

After running the Monkey, follow the Monkeys’ actions on the Monkey Island’s infection map.

Now you can match this activity from the Monkey timeline display to your internal SIEM and make sure your security
 solutions are identifying and correctly alerting on different attacks.

- The red arrows indicate successful exploitations. If you see red arrows, those incidents ought to be reported as
 exploitation attempts, so check whether you are receiving alerts from your security systems as expected.
- The orange arrows indicate scanning activity, usually used by attackers to locate potential vulnerabilities.
 If you see orange arrows, those incidents ought to be reported as scanning attempts (and possibly as segmentation violations).
- The blue arrows indicate tunneling activity, usually used by attackers to infiltrate “protected” networks from
 the Internet. Perhaps someone is trying to bypass your firewall to gain access to a protected service in your network?
 Check if your micro-segmentation / firewall solution identify or report anything.

While running this scenario, be on the lookout for the action that should arise:
 Did you get a phone call telling you about suspicious activity inside your network? Are events flowing
 into your security events aggregators? Are you getting emails from your IR teams?
 Is the endpoint protection software you installed on machines in the network reporting on anything? Are your
 compliance scanners detecting anything wrong?
 
Lastly, check Zero Trust and Mitre ATT&CK reports, to see which attacks can be executed on the network and how to
 fix it.
 
 ![Map](/images/usage/scenarios/map-full-cropped.png "Map")
