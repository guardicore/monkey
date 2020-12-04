---
title: "MITRE ATT&CK assessment"
date: 2020-10-22T16:58:22+03:00
draft: false
description: "Assess your network security detection and prevention capabilities."
weight: 2
---

## Overview 

Infection Monkey can simulate various [ATT&CK](https://attack.mitre.org/matrices/enterprise/) techniques on the network. 
Use it to assess your security solutions’ detection and prevention capabilities. Infection Monkey will help you find 
which ATT&CK techniques go unnoticed and will provide recommendations about preventing them.


## Configuration

- **ATT&CK matrix** You can use ATT&CK configuration section to select which techniques you want the Monkey to simulate. 
Leave default settings for the full simulation.
- **Exploits -> Credentials** This configuration value will be used for brute-forcing. We use most popular passwords 
and usernames, but feel free to adjust it according to the default passwords used in your network. Keep in mind that 
long lists means longer scanning times.
- **Network -> Scope** Disable “Local network scan” and instead provide specific network ranges in 
the “Scan target list”.

![ATT&CK matrix](/images/usage/scenarios/attack-matrix.png "ATT&CK matrix")

## Suggested run mode

Run the Infection Monkey on as many machines in your environment as you can to get a better assessment. This can be easily 
achieved by selecting the “Manual” run option and executing the command shown on different machines in your environment 
manually or with your deployment tool.

## Assessing results

The **ATT&CK Report** shows the status of ATT&CK techniques simulations. Click on any technique to see more details 
about it and potential mitigations. Keep in mind that each technique display contains a question mark symbol that 
will take you to the official documentation of ATT&CK technique, where you can learn more about it.
