---
title: "Zero Trust assessment"
date: 2020-10-22T16:58:09+03:00
draft: false
description: "See where you stand in your Zero Trust journey."
weight: 1
---

## Overview

Want to assess your progress in achieving a Zero Trust network? The Infection Monkey can automatically evaluate your readiness across the different
[Zero Trust Extended Framework](https://www.forrester.com/report/The+Zero+Trust+eXtended+ZTX+Ecosystem/-/E-RES137210) principles.

## Configuration

- **Propagation -> Credentials** This configuration value will be used for brute-forcing. The Infection Monkey uses the most popular default passwords and usernames, but feel free to adjust it according to the default passwords common in your network. Keep in mind a longer list means longer scanning times.
- **Propagation -> Network analysis -> Network** Disable “Scan Agent's networks” and instead provide specific network ranges in the “Scan target list.”
- **Propagation -> Network analysis -> Network segmentation testing** This configuration setting allows you to define
subnets that should be segregated from each other.

In general, other configuration value defaults should be good enough, but feel free to see the “Other” section for tips and tricks about more features and in-depth configuration parameters you can use.

![Exploit password and user lists](/images/usage/scenarios/user-password-lists.png "Exploit password and user lists")

## Suggested run mode

Run the Infection Monkey on as many machines as you can. You can easily achieve this by selecting the “Manual” run option and executing the command shown on different machines in your environment manually or with your deployment tool. Additionally, you can use any other run options you see fit.

## Assessing results

You can see your results in the Zero Trust report section. “The Summary” section will give you an idea about which Zero Trust pillars were the Infection Monkey tested, how many tests were performed and test statuses. Specific tests are described in the “Test Results” section. The “Findings” section shows details about the Monkey actions. Click on “Events” of different findings to observe what exactly the Infection Monkey did and when it did it. This should make it easy to cross reference events with your security solutions and alerts/logs.
