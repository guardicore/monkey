---
title: "SSH"
date: 2023-09-13T16:51:38+05:30
tags: ["credentials collector", "ssh", "linux"]
weight: 3
---

## Description

The SSH Credentials Collector steals SSH keys from Linux users.

For all users on the system, it locates the `/home/<user>/.ssh`
directory and steals keypairs from it. The supported private key
encryption formats are RSA, DSA, EC, and ECDSA.
