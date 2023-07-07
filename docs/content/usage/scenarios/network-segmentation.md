---
title: "Network Segmentation"
date: 2020-08-12T13:05:05+03:00
draft: false
description: "Verify your network is properly segmented."
weight: 4
---

## Overview

Segmentation is a method of creating secure zones in data centers and cloud deployments. It allows organizations to isolate workloads from one another and secure them individually, typically using policies. A useful way to test your company's segmentation effectiveness is to ensure that your network segments are properly separated (e.g., your development environment is isolated from your production environment and your applications are isolated from one another).

[Segmentation is key](https://www.akamai.com/products/akamai-segmentation/use-cases) to protecting your network. It can reduce the network's attack surface and minimize the damage caused during a breach.

You can use the Infection Monkey's cross-segment traffic feature to verify that your network segmentation configuration is adequate. This way, you can ensure that, even if a bad actor breaches your defenses, they can't move laterally between segments.


## Configuration

- **Propagation -> Network analysis -> Network segmentation testing** This configuration setting allows you to define
 subnets that should be segregated from each other. If any of the provided networks can reach each other, you'll see it
 in the security report. The networks configured in this section will be scanned using `ping`.
- **(Optional) Propagation -> Network analysis -> Network** You can disable **Scan Agent's networks** and leave all other options at the default setting if you only want to test for network segmentation without any lateral movement.

## Suggested run mode

Execute The Infection Monkey on machines in different subnetworks using the "Manual" run option.

 Note that if the Infection Monkey can't communicate to the Monkey Island, it will
 not be able to send scan results, so make sure all machines can reach the Monkey Island.

![How to configure network segmentation testing](/images/island/configuration_page/segmentation_configuration.png "How to configure network segmentation testing")

## Assessing results

Check the Infection Map and Security Report for segmentation problems. Ideally, all scanned nodes should only have edges with the Monkey Island Server.

![Map](/images/island/infection_map_page/segmentation_map.png "Map")
