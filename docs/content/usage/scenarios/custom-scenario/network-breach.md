---
title: "Network Breach"
date: 2020-08-12T13:04:55+03:00
draft: false
description: "Simulate an internal network breach and assess the potential impact."
weight: 3
---

## Overview

From the [Hex-Men campaign](https://web.archive.org/web/20210115171355/https://www.guardicore.com/2017/12/beware-the-hex-men/) that hit
internet-facing DB servers to a [cryptomining operation that attacks WordPress sites](https://web.archive.org/web/20210115185135/https://www.guardicore.com/2018/06/operation-prowli-traffic-manipulation-cryptocurrency-mining-2/) or any other malicious campaign – attackers are now trying to go deeper into your network.

Infection Monkey will help you assess the impact of a future breach by attempting to propagate within your internal network using service vulnerabilities, brute-forcing and other safe exploiters.

## Configuration

- **Exploits -> Exploits** Here you can review the exploits the Infection Monkey will be using. By default all
safe exploiters are selected.
- **Exploits -> Credentials** This configuration value will be used for brute-forcing. The Infection Monkey uses the most popular default passwords and usernames, but feel free to adjust it according to the default passwords common in your network. Keep in mind a longer list means longer scanning times.
- **Network -> Scope** Make sure to properly configure the scope of the scan. You can select **Local network scan**
 and allow Monkey to propagate until maximum **Scan depth**(hop count) is reached, or you can fine tune it by providing
 specific network ranges in **Scan target list**. Scanning a local network is more realistic, but providing specific
 targets will make the scanning process substantially faster.
- **(Optional) Internal -> Network -> TCP scanner** Here you can add custom ports your organization is using.
- **(Optional) Monkey -> Post-Breach Actions** If you only want to test propagation in the network, you can turn off
all post-breach actions. These actions simulate an attacker's behavior after getting access to a new system but in no
 way helps the Infection Monkey exploit new machines.

![Exploiter selector](/images/usage/use-cases/network-breach.PNG "Exploiter selector")

## Suggested run mode

Decide which machines you want to simulate a breach on and use the “Manual” run option to start the Infection Monkey on them.
Use administrative privileges to run the Infection Monkey to simulate an attacker that was able to elevate their privileges.
You could also simulate an attack initiated from an unidentified machine connected to the network (e.g., a technician
laptop or third-party vendor machine) by running the Infection Monkey on a dedicated machine with an IP in the network you
wish to test.


## Assessing results

Check the infection map and Security report to see how far The Infection Monkey managed to propagate in your network and which
vulnerabilities it successfully exploited. If you left post-breach actions selected, you should also check the MITRE ATT&CK and
Zero Trust reports for more details.

![Map](/images/usage/use-cases/map-full-cropped.png "Map")
