---
title: "Network Breach"
date: 2020-08-12T13:04:55+03:00
draft: false
description: "Simulate an internal network breach and assess the potential impact."
weight: 1
---

## Overview 

Whether it was the [Hex-men campaign](https://www.guardicore.com/2017/12/beware-the-hex-men/) that hit your 
Internet-facing DB server, a [cryptomining operation that attacked your WordPress site](https://www.guardicore.com/2018/06/operation-prowli-traffic-manipulation-cryptocurrency-mining-2/) 
or any other malicious campaign – the attackers are now trying to go deeper into your network.

Infection Monkey will help you assess the impact of internal network breach, by trying to propagate within it
 using service vulnerabilities, brute-forcing and other safe attack methods.

## Configuration

#### Important configuration values:
- **Exploits -> Exploits** You can review the exploits Infection Monkey will be using. By default all 
safe exploiters are selected.
- **Exploits -> Credentials** This configuration value will be used for brute-forcing. We use most popular passwords
 and usernames, but feel free to adjust it according to your native language and other factors. Keep in mind that long 
 lists means longer scanning times.
- **Network -> Scope** Make sure to properly configure the scope of the scan. You can select **Local network scan**
 and allow Monkey to propagate until maximum **Scan depth**(hop count) is reached or you can fine tune it by providing 
 specific network ranges in **Scan target list**. Scanning local network is more realistic, but providing specific 
 targets will make scanning process substantially faster.
- **(Optional) Internal -> Network -> TCP scanner** You can add custom ports your organization is using.
- **(Optional) Monkey -> Post Breach Actions** If you only want to test propagation in the network, you can turn off 
all post breach actions. These actions simulate attacker's behaviour after getting access to a new system, but in no
 way helps to exploit new machines.

![Exploiter selector](/images/usage/use-cases/network-breach.PNG "Exploiter selector")

## Assessing results

Check infection map and security report to see how far monkey managed to propagate in the network and which 
vulnerabilities it used in doing so. If you left post breach actions selected, you should also check ATT&CK and 
Zero Trust reports.

![Map](/images/usage/use-cases/map-full-cropped.png "Map")
