---
title: "ATT&CK techniques"
date: 2020-10-22T16:58:22+03:00
draft: false
description: "Find issues related to Zero Trust Extended framework compliance."
weight: 1
---

## Overview 

Infection Monkey can simulate a number of realistic ATT&CK techniques on the network automatically. This will help you 
assess the capabilities of your defensive solutions and see which ATT&CK techniques go unnoticed and how to prevent 
them.

## Configuration

- **ATT&CK matrix** You can use ATT&CK configuration section to select which techniques you want to scan. Keep in mind 
that ATT&CK matrix configuration just changes the overall configuration by modifying related fields, thus you should 
start by modifying and saving the matrix. After that you can change credentials and scope of the scan, but exploiters, 
post breach actions and other configuration values will be already chosen based on the ATT&CK matrix and shouldn’t be 
modified.
- **Exploits -> Credentials** This configuration value will be used for brute-forcing. We use most popular passwords 
and usernames, but feel free to adjust it according to your native language and other factors. Keep in mind that long 
lists means longer scanning times.
- **Network -> Scope** Make sure to properly configure the scope of the scan. You can select Local network scan and 
allow Monkey to propagate until maximum Scan depth(hop count) is reached or you can fine tune it by providing specific 
network ranges in Scan target list. Scanning the local network is more realistic, but providing specific targets will 
make the scanning process substantially faster.

![ATT&CK matrix](/images/usage/scenarios/attack-matrix.png "ATT&CK matrix")

## Suggested run mode

You should run the Monkey on network machines with defensive solutions you want to test.

A lot of ATT&CK techniques have a scope of a single node, so it’s important to manually run monkeys for better coverage.

## Assessing results

See the **ATT&CK report** to assess results of ATT&CK techniques used in your network. Each technique in the result 
matrix is colour coated according to it’s status. Click on any technique to see more details about it and potential 
mitigations. Keep in mind that each technique display contains a question mark symbol that will take you to the 
official documentation of ATT&CK technique, where you can learn more about it.

