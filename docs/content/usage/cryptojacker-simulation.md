---
title: " Cryptojacker Simulation"
date: 2022-08-09T13:51:13-04:00
draft: false
description: "Simulate a cryptojacking attack on your network and assess the potential damage."
weight: 6
pre: "<i class='fa fa-coins'></i> "
---

The Infection Monkey is capable of simulating the behavior of a cryptojacker by
using the CPU and memory of infected systems to perform cryptographic
operations. It can also send network requests that imitate bitcoin mining
network traffic.

## Production safety

This module is not considered to be safe for production environments because
it can consume large amounts of CPU and RAM. If the module is configured to
consume excessive amounts of CPU and RAM, it may cause some systems or services
to become unstable. Users are advised to use caution when setting the CPU and
memory utilization options so as not to negatively impact production
environments.

## Configuration options
![Cryptojacker configuration](/images/island/configuration_page/cryptojacker_configuration.png "Cryptojacker configuration")
### Duration
This option controls how long the cryptojacking simulation will run. The
simulation will automatically shut itself down after the configured time has
elapsed.

### CPU utilization
The cryptojacking simulation will attempt to consume the specified percentage
of a single CPU core.

### Memory utilization
The cryptojacking simulation will attempt to consume the specified percentage
of system RAM. Note that an internal safeguard prevents this component from
consuming more than 90% of the available RAM. Therefore, while specifying 100%
is possible, this component has a theoretical upper limit that prevents it from
consuming more than 90% of total system RAM.

### Simulate bitcoin mining network traffic
If enabled, the cryptojacking simulation will send bitcoin `getblocktemplate`
requests via HTTP over the network to the Island. This can help verify that
NIDSs are working properly.
