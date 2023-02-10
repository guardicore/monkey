---
title: "Agent propagation"
date: 2022-06-03T13:17:22+05:30
draft: false
pre: '<i class="fas fa-user-secret"></i> '
weight: 2
tags: ["agent", "propagation", "reference"]
---

## How does the Infection Monkey Agent propagate to a new machine?

The Agent propagates using remote code execution vulnerabilities. Once the
Agent has achieved remote code execution on the victim, it executes commands
that are similar to the ones described in the [manual run
page](../../usage/running-manually/).

On Windows targets, the Agent is copied to `C:\Windows\temp\monkey64-<random_string>.exe`.
On Linux targets, it is copied to `/tmp/monkey-<random_string>`.
