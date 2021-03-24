---
title: "Infection Monkey Documentation Hub"
date: 2020-05-26T18:15:37+03:00
draft: false
---

# Infection Monkey documentation hub

{{< homepage_shortcuts >}}

## What is Guardicore Infection Monkey?

The Infection Monkey is an open source breach and attack simulation tool for testing a data center's resiliency to perimeter breaches and internal server infection.
Infection Monkey will help you test implemented security solutions and will provide visibility of the internal network through the eyes of an attacker.

Infection Monkey is free and can be downloaded from [our homepage](https://infectionmonkey.com/).

![Infection Monkey Documentation Hub Logo](/images/monkey-teacher.svg?height=400px "Infection Monkey Documentation Hub Logo")

## How it works

Architecturally Infection Monkey tool is comprised of two parts:

* Monkey Agent (Monkey for short) - a safe, worm like binary program which scans, spreads and simulates attack techniques on the **local network**.
* Monkey Island Server (Island for short) - a C&C web server which serves GUI for users and interacts with Monkey Agents.

User runs Monkey Agent on the Island server machine or distributes Monkey Agent binaries on the network manually. Based on 
the configuration parameters, Monkey Agents scan, propagate and simulate attackers behaviour on the local network. All of the 
information gathered about the network is aggregated in the Island Server and displayed once all Monkey Agents are finished.

## Results

Results of running Monkey Agents are:
 - A map which displays how much of the network attacker can see, services accessible and potential propagation routes.
 - Security report, which displays security issues Monkey Agents found and/or exploited.
 - Mitre ATT&CK report, which displays the outcomes of ATT&CK techniques Monkey Agents tried to use.
 - Zero Trust report, which displays violations of Zero Trust principles that Agents found.
 
More in depth description of reports generated can be found in [reports documentation page](/reports)

## Getting Started

If you haven't downloaded Infection Monkey yet you can do so [from our homepage](https://www.guardicore.com/infectionmonkey/#download). After downloading the Monkey, install it using one of our [setup guides](setup), and read our [getting started guide](usage/getting-started) for a quick-start on Monkey!

## Support and community

If you need help or want to talk all things Monkey, you can [join our public Slack workspace](https://join.slack.com/t/infectionmonkey/shared_invite/enQtNDU5MjAxMjg1MjU1LWM0NjVmNWE2ZTMzYzAxOWJiYmMxMzU0NWU3NmUxYjcyNjk0YWY2MDkwODk4NGMyNDU4NzA4MDljOWNmZWViNDU) or [contact us via Email](mailto:support@infectionmonkey.com).
