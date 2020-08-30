---
title: "Credential Leak"
date: 2020-08-12T13:04:25+03:00
draft: false
description: "Assess the impact of successful phishing attack, insider threat, or other form of credentials leak."
weight: 4
---

## Overview 

Numerous attack techniques(from phishing to dumpster diving) might result in a credential leak, 
which can be **extremely costly** as demonstrated in our report [IResponse to IEncrypt](https://www.guardicore.com/2019/04/iresponse-to-iencrypt/).

Infection Monkey can help assess the impact of stolen credentials by automatically searching 
where these credentials can be reused.

## Configuration

#### Important configuration values:

- **Exploits -> Credentials** After setting up the Island add the users’ **real** credentials 
(usernames and passwords) to the Monkey’s configuration (Don’t worry, this sensitive data is not accessible and is not
 distributed or used in any way other than being sent to the monkeys, and can be easily eliminated by resetting the Monkey Island’s configuration).
- **Internal -> Exploits -> SSH keypair list** Monkey automatically gathers SSH keys on the current system. 
For this to work, Monkey Island or initial Monkey needs to have access to SSH key files(grant permission or run Monkey as root).
To make sure SSH keys were gathered successfully, refresh the page and check this configuration value after you run the Monkey
(content of keys will not be displayed, it will appear as `<Object>`).

To simulate the damage from a successful phishing attack using the Infection Monkey, choose machines in your network 
from potentially problematic group of machines, such as the laptop of one of your heavy email users or 
one of your strong IT users (think of people who are more likely to correspond with people outside of 
your organization). Execute the Monkey on chosen machines by clicking on “**1. Run Monkey**” from the left sidebar menu
 and choosing “**Run on machine of your choice**”.

![Exploit password and user lists](/images/usage/scenarios/user-password-lists.png "Exploit password and user lists")

## Assessing results

To assess the impact of leaked credentials see Security report. It's possible, that credential leak resulted in even
more leaked credentials, for that look into **Security report -> Stolen credentials**. 
