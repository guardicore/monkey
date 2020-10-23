---
title: "Credentials Leak"
date: 2020-08-12T13:04:25+03:00
draft: false
description: "Assess the impact of a successful phishing attack, insider threat, or other form of credentials leak."
weight: 5
---

## Overview 

Numerous attack techniques(from phishing to dumpster diving) might result in a credential leak, 
which can be **extremely costly** as demonstrated in our report [IResponse to IEncrypt](https://www.guardicore.com/2019/04/iresponse-to-iencrypt/).

Infection Monkey can help assess the impact of stolen credentials by automatically searching 
where these credentials can be reused.

## Configuration

- **Exploits -> Credentials** After setting up the Island add the users’ **real** credentials 
(usernames and passwords) to the Monkey’s configuration (Don’t worry, this sensitive data is not accessible and is not
 distributed or used in any way other than being sent to the monkeys, and can be easily eliminated by resetting the Monkey Island’s configuration).
- **Internal -> Exploits -> SSH keypair list** Monkey automatically gathers SSH keys on the current system. 
For this to work, Monkey Island or initial Monkey needs to have access to SSH key files(grant permission or run Monkey as root).
To make sure SSH keys were gathered successfully, refresh the page and check this configuration value after you run the Monkey
(content of keys will not be displayed, it will appear as `<Object>`).

## Suggested run mode

Execute the Monkey on a chosen machine in your network using the “Manual” run option. 
Run the Monkey as a privileged user to make sure it gathers as many credentials from the system as possible.

![Exploit password and user lists](/images/usage/scenarios/user-password-lists.png "Exploit password and user lists")

## Assessing results

To assess the impact of leaked credentials see Security report. It's possible that credential leak resulted in even
more leaked credentials, for that look into **Security report -> Stolen credentials**. 
