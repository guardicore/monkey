---
title: "Network Segmentation"
date: 2020-08-12T13:05:05+03:00
draft: false
description: "Test network segmentation policies for apps that need ringfencing or tiers that require microsegmentation."
weight: 3
---

## Overview 

Segmentation is a method of creating secure zones in data centers and cloud deployments that allows companies to
 isolate workloads from one another and secure them individually, typically using policies.
 A useful way to test the effectiveness of your segmentation is to ensure that your network segments are
 properly separated, e,g, your Development is separated from your Production, your applications are separated from one
 another etc. To security test is to verify that your network segmentation is configured properly. This way you make
 sure that even if a certain attacker has breached your defenses, it can’t move laterally from point A to point B.

[Segmentation is key](https://www.guardicore.com/use-cases/micro-segmentation/) to protecting your network, reducing 
the attack surface and minimizing the damage of a breach. The Monkey can help you test your segmentation settings with 
its cross-segment traffic testing feature.

## Configuration

#### Important configuration values:

- **Network -> Network analysis -> Network segmentation testing** This configuration setting allows you to define
 subnets that should be segregated from each other. If any of provided networks can reach each other, you'll see it 
 in security report.
- **(Optional) Network -> Scope** You can disable **Local network scan** and leave other options by default if you only want to
 test for network segmentation without any lateral movement.
- **(Optional) Monkey -> Post Breach Actions** If you only want to test segmentation in the network, you can turn off 
all post breach actions. These actions simulate attacker's behaviour after getting access to a new system, so they
 might trigger your defence solutions which will interrupt segmentation test.

Execute Monkeys on machines in different subnetworks manually, by choosing “**1. Run Monkey**” from the left sidebar menu
 and clicking on “**Run on machine of your choice**”. 
 Alternatively, you could provide valid credentials and allow Monkey to propagate to relevant subnetworks by itself. 
 
 Note that if Monkey can't communicate to the Island, it will
 not be able to send scan results, so make sure all machines can reach the island. 

![How to configure network segmentation testing](/images/usage/scenarios/segmentation-config.png "How to configure network segmentation testing")


## Assessing results

Check infection map and security report for segmentation problems. Ideally, all scanned nodes should only have
 edges with the Island Server.

![Map](/images/usage/use-cases/segmentation-map.PNG "Map")

