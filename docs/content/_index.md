---
title: "Infection Monkey Documentation Hub"
date: 2020-05-26T18:15:37+03:00
draft: false
---

# Infection Monkey documentation hub

{{< homepage_shortcuts >}}

## What is Guardicore Infection Monkey?

The Infection Monkey is an open-source breach and attack simulation tool for
testing a data center's resiliency to perimeter breaches and internal server
infection. Infection Monkey will help you validate existing security solutions
and will provide a view of the internal network from an attacker's perspective.

Infection Monkey is free and can be downloaded from [our
homepage](https://www.akamai.com/infectionmonkey).

![Infection Monkey Documentation Hub
Logo](/images/monkey-teacher.svg?height=400px "Infection Monkey Documentation
Hub Logo")

## How it works

Architecturally, Infection Monkey comprises two components:

* Monkey Agent (Monkey for short) - a safe, worm-like binary program which
  scans, propagates and simulates attack techniques on the **local network**.
* Monkey Island Server (Island for short) - a C&C web server which provides a
  GUI for users and interacts with the Monkey Agents.

The user can run the Monkey Agent on the Island Server machine or distribute
Monkey Agent binaries on the network manually. Based on the configuration
parameters, Monkey Agents scan, propagate and simulate an attacker's behavior
on the local network. All the information gathered about the network is
aggregated in the Island Server and displayed once all Monkey Agents are
finished.

## Results

The results of running Monkey Agents are:
 - A map which displays how much of the network an attacker can see, what
   services are accessible and potential propagation routes.
 - A report, which displays security issues that Monkey Agents
   discovered and/or exploited.

A more in-depth description of reports generated can be found in the [reports
documentation page]({{< ref "/reports" >}}).

## Getting Started

If you haven't downloaded Infection Monkey yet you can do so [from our
homepage](https://www.akamai.com/infectionmonkey#download). After downloading
the Monkey, install it using one of our [setup guides]({{< ref "/setup" >}}),
and read our [getting started guide]({{< ref "/usage/getting-started" >}}) for
a quick-start on Monkey!

## Support and community

If you need help or want to talk all things Monkey, you can [join our public
Slack
workspace](https://join.slack.com/t/infectionmonkey/shared_invite/enQtNDU5MjAxMjg1MjU1LWM0NjVmNWE2ZTMzYzAxOWJiYmMxMzU0NWU3NmUxYjcyNjk0YWY2MDkwODk4NGMyNDU4NzA4MDljOWNmZWViNDU)
or [contact us via Email](mailto:support@infectionmonkey.com).
