---
title: "Agent propagation"
date: 2022-06-03T13:17:22+05:30
draft: false
pre: '<i class="fas fa-user-secret"></i> '
weight: 2
tags: ["agent", "propagation", "reference"]
---

## How does the Infection Monkey Agent propagate to a new machine?

Agent mainly propagates using remote code execution vulnerabilities. Once the agent is able to
run commands on the victim it executes commands that are similar to the ones described in [manual run page.](../../usage/running-manually/)

On Windows, it is copied to `C:\Windows\temp\monkey64.exe`. On Linux, it is copied to `/tmp/monkey`.
