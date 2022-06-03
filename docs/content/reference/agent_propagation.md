---
title: "Agent propagation"
date: 2022-06-03T13:17:22+05:30
draft: false
pre: '<i class="fas fa-user-secret"></i> '
weight: 2
tags: ["agent", "propagation", "reference"]
---

## How does the Infection Monkey Agent propagate to a new machine?

Once an Agent exploits a vulnerable system, it propagates to the machine by copying the appropriate
Agent binary to it.

On Windows, it is copied to `C:\Windows\temp\monkey64.exe`. On Linux, it is copied to `/tmp/monkey`.
