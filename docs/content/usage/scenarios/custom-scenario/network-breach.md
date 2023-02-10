---
title: "Network Breach"
date: 2020-08-12T13:04:55+03:00
draft: false
description: "Simulate an internal network breach and assess the potential impact."
weight: 3
---

## Overview

From the [Hex-Men
campaign](https://web.archive.org/web/20210115171355/https://www.guardicore.com/2017/12/beware-the-hex-men/)
that hit internet-facing DB servers to a [cryptomining operation that attacks
WordPress
sites](https://web.archive.org/web/20210115185135/https://www.guardicore.com/2018/06/operation-prowli-traffic-manipulation-cryptocurrency-mining-2/)
or any other malicious campaign – attackers are now trying to go deeper into
your network.

Infection Monkey will help you assess the impact of a future breach by
attempting to propagate within your internal network using service
vulnerabilities, brute-forcing and other safe exploiters.

## Configuration

- **Propagation -> Propagation** Here you can review the exploits the Infection
  Monkey will be using. By default all safe exploiters are selected.
- **Propagation -> Credentials** This configuration value will be used for
  brute-forcing. The Infection Monkey uses the most popular default passwords
  and usernames, but feel free to adjust it according to the default passwords
  common in your network. Keep in mind a longer list means longer scanning
  times.
- **Propagation -> Network analysis -> Network** Make sure to properly
  configure the scope of the scan. You can select **Scan Agent's networks** and
  allow Monkey to propagate until **Maximum scan depth** (hop count) is reached,
  or you can fine tune it by providing specific network ranges in **Scan target
  list**. Scanning a local network is more realistic, but providing specific
  targets will make the scanning process substantially faster.
  - **Maximum scan depth** can be configured from the **Propagation ->
    General** tab.
- **(Optional) Propagation -> Network Analysis -> TCP scanner** Here you can
  add custom ports your organization is using.

![Exploiter selector](/images/island/configuration_page/propagation_configuration.png "Exploiter
selector")

## Suggested run mode

Decide which machines you want to simulate a breach on and use the "Manual" run
option to start the Infection Monkey Agent on them. Use administrative privileges to
run the Infection Monkey to simulate an attacker that was able to elevate their
privileges. You could also simulate an attack initiated from an unidentified
machine connected to the network (e.g., a technician laptop or third-party
vendor machine) by running the Infection Monkey on a dedicated machine with an
IP in the network you wish to test.


## Assessing results

Check the Infection Map and Security Report to see how far Infection Monkey
managed to propagate in your network and which vulnerabilities it successfully
exploited.

![Map](/images/island/infection_map_page/infection_map.png "Map")
