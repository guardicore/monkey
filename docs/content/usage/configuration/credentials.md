---
title: "Credentials"
date: 2020-06-09T12:20:08+03:00
draft: false
description: "Configure credentials that the Infection Monkey will use for propagation."
---

On this screen, you can configure credentials for Infection Monkey to use in the propagation
stage. These can be anything from default or weak passwords, to "stolen" credentials from your
network, simulating an attacker with inside knowledge.

All possible credential combinations will be tried for propagation. Identity-secret pairs added
in the same row will be attempted before any other credential combinations.

Note that to add a credential, it is not necessary to fill out all the fields.

![Configure credentials](/images/island/configuration_page/credentials_configuration.png "Configure credentials")
