---
title: "Zero Trust assessment"
date: 2020-10-22T16:58:09+03:00
draft: false
description: "See where you are in your Zero Trust journey."
weight: 0
---

## Overview 

Infection Monkey can help assess your network compliance with Zero Trust Extended framework by checking for various 
violations of Zero Trust principles.

## Configuration

- **Exploits -> Credentials** This configuration value will be used for brute-forcing. We use most popular passwords 
and usernames, but feel free to adjust it according to your native language and other factors. Keep in mind that long 
lists means longer scanning times.
- **Network -> Scope** Make sure to properly configure the scope of the scan. You can select Local network scan and 
allow Monkey to propagate until maximum Scan depth(hop count) is reached or you can fine tune it by providing specific 
network ranges in Scan target list. Scanning local network is more realistic, but providing specific targets will make 
the scanning process substantially faster.
- **Network -> Network analysis -> Network segmentation testing** This configuration setting allows you to define 
subnets that should be segregated from each other.

In general, other configuration value defaults should be good enough, but feel free to see the “Other” section 
for tips and tricks about other features and in-depth configuration parameters you can use.

![Exploit password and user lists](/images/usage/scenarios/user-password-lists.png "Exploit password and user lists")

## Suggested run mode

Running Monkey from the Island alone will give you reasonable results, but to increase the coverage for segmentation 
and single node tests make sure to run monkey manually on various machines in the network. The more machines monkey 
runs on, the better the coverage.

## Assessing results

See the results in the Zero Trust report section. “The Summary” section will give you an idea about which Zero Trust 
pillars were tested, how many tests were done and test statuses. You can see more details below in the “Test Results” 
section, where each test is sorted by pillars and principles it tests. To get even more details about what Monkey did,
 go down to the “Findings” section and observe “Events” of different findings. “Events” will tell you what exactly 
 Infection Monkey did and when it was done, to make it easy to cross reference it with your defensive solutions.
