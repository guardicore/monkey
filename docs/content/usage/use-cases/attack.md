---
title: "MITRE ATT&CK assessment"
date: 2020-10-22T16:58:22+03:00
draft: false
description: "Assess your network security detection and prevention capabilities."
weight: 2
---

## Overview 

The Infection Monkey can simulate various [ATT&CK](https://attack.mitre.org/matrices/enterprise/) techniques on the network. Use it to assess your security solutions' detection and prevention capabilities. The Infection Monkey will help you find which ATT&CK techniques go unnoticed and provide recommendations along with suggested mitigations.


## Configuration

- **ATT&CK matrix** You can use the ATT&CK configuration section to select which techniques you want the Infection Monkey to simulate. 
Leave default settings for the full simulation.
- **Exploits -> Credentials** This configuration value will be used for brute-forcing. The Infection Monkey uses the most popular default passwords and usernames, but feel free to adjust it according to the default passwords common in your network. Keep in mind a longer list means longer scanning times.
- **Network -> Scope** Disable “Local network scan” and instead provide specific network ranges in the “Scan target list”.

![ATT&CK matrix](/images/usage/scenarios/attack-matrix.png "ATT&CK matrix")

## Suggested run mode

Run the Infection Monkey on as many machines as you can. You can easily achieve this by selecting the “Manual” run option and executing the command shown on different machines in your environment manually or with your deployment tool. Additionally, you can use any other run options you see fit.

## Assessing results

The **ATT&CK Report** shows the status of simulations using ATT&CK techniques. Click on a technique to see more details about it and potential mitigations. Keep in mind that each technique display contains a question mark symbol that will take you to the official documentation of the specific ATT&CK technique used, where you can learn more about it.
