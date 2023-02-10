---
title: "Other"
date: 2020-08-12T13:07:55+03:00
draft: false
description: "Tips and tricks about configuring Monkeys for your needs."
weight: 100
---

## Overview
This page provides additional information about configuring the Infection
Monkey, tips and tricks, and creative usage scenarios.

## Accelerate the test

To improve scanning speed you could **specify a subnet instead of scanning all
of the local network**.

The following configuration values also have an impact on scanning speed:
- **Propagation -> Credentials** - The more usernames and passwords you input,
  the longer it will take the Infection Monkey to scan machines that have
  remote access services. The Infection Monkey Agents try to stay elusive and
  leave a low impact, and thus brute-forcing takes longer than with loud
  conventional tools.
- **Propagation -> Network analysis -> Network** - Scanning large networks with
  a lot of propagations can become unwieldy. Instead, try to scan your networks
  bit by bit with multiple runs.
- **Propagation -> Network analysis -> TCP scanner** - Here you can trim down
  the list of ports the Infection Monkey tries to scan, improving performance.

## Combining different scenarios

The Infection Monkey is not limited to the scenarios mentioned in this section.
Once you get the hang of configuring it, you might come up with your own use
case or test all of the suggested scenarios at the same time! Whatever you do,
the Infection Monkey's Security report will be waiting for you with your
results!

## Credentials

Every network has its old "skeleton keys" that it should have long discarded.
Configuring the Infection Monkey with old and stale passwords will enable you
to ensure they were really discarded.

To add the old passwords, go to the Monkey Island's **Exploit password list**
under **Propagation -> Credentials** and use the "+" button to add the old
passwords to the configuration. For example, here we added a few extra
passwords (and a username as well) to the configuration:

![Exploit password and user lists](/images/island/configuration_page/credentials_configuration.png "Exploit password and user lists")
