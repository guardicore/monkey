---
title: "How to Configure the Monkey"
date: 2020-06-07T19:08:51+03:00
draft: false
weight: 3
---

The Monkey is very configurable, nearly every part of it can be modified to turn it to a fast acting worm or into a port scanning and system information collecting machine.

The configuration is split into two parts, **Basic** and everything else. The **Basic** options are pretty self explanatory and are split into two sections:

## Credentials

In this screen you can feed the Monkey with “stolen” credentials for your network, simulating an attacker with inside knowledge.

## Network

Here you can control multiple important settings, such as:

* Network propagation depth - How many hops from the base machine will the Monkey spread
* Local network scan - Should the Monkey attempt to attack any machine in its subnet
* Scanner IP/subnet list - Specific IP ranges that the Monkey should try to attack.
