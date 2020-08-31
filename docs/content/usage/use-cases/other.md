---
title: "Other"
date: 2020-08-12T13:07:55+03:00
draft: false
description: "Tips and tricks about configuring monkey for your needs."
weight: 100
---

## Overview 

This page provides additional information about configuring monkeys, tips and tricks and creative usage scenarios.

## ATT&CK & Zero Trust scanning

You can use **ATT&CK** configuration section to select which techniques you want to scan. Keep in mind that ATT&CK
 matrix configuration just changes the overall configuration by modifying related fields, thus you should start by
 modifying and saving the matrix. After that you can change credentials and scope of the scan, but exploiters,
 post breach actions and other configuration values will be already chosen based on ATT&CK matrix and shouldn't be
 modified.
 
There's currently no way to configure monkey using Zero Trust framework, but regardless of configuration options,
 you'll always be able to see ATT&CK and Zero Trust reports.

## Tips and tricks

- Use **Monkey -> Persistent scanning** configuration section to either have periodic scans or to increase
 reliability of exploitations.
 
- To increase propagation run monkey as root/administrator. This will ensure that monkey will gather credentials
 on current system and use them to move laterally.

- Every network has its old “skeleton keys” that should have long been discarded. Configure the Monkey with old and stale passwords, but make sure that they were really discarded using the Monkey. To add the old passwords, in the island’s configuration, go to the “Exploit password list” under “Basic - Credentials” and use the “+” button to add the old passwords to the configuration. For example, here we added a few extra passwords (and a username as well) to the configuration:

![Exploit password and user lists](/images/usage/scenarios/user-password-lists.png "Exploit password and user lists")

- To see the Monkey executing in real-time on your servers, add the **post-breach action** command: `wall “Infection Monkey was here”`. This post breach command will broadcast a message across all open terminals on the servers the Monkey breached, to achieve the following: Let you know the Monkey ran successfully on the server. let you follow the breach “live” alongside the infection map, and check which terminals are logged and monitored inside your network. See below:

![How to configure post breach commands](/images/usage/scenarios/pba-example.png "How to configure post breach commands.")

- If you're scanning a large network, consider narrowing the scope and scanning it bit by bit if scan times become too
 long. Lowering the amount of credentials, exploiters or post breach actions can also help to lower scanning times.

