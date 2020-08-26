---
title: "IDS/IPS Test"
date: 2020-08-12T13:07:47+03:00
draft: false
description: "Test your network defence solutions."
weight: 5
---

## Overview 

The Infection Monkey can help you verify that your security solutions are working the way you expected them to.
 These may include your IR and SOC teams, your SIEM, your firewall, your endpoint security solution, and more.

## Configuration

#### Important configuration values:

- **Monkey -> Post breach** Post breach actions simulate the actions an attacker would make on infected system.
 To test something not present on the tool, you can provide your own file or command to be ran. 

The default configuration is good enough for many cases, but configuring testing scope and adding brute-force
 credentials is a good bet in any scenario. 
 
Running the Monkey on both the Island and on a few other machines in the network manually is also recommended,
 as it increases coverage and propagation rates.


![Post breach configuration](/images/usage/use-cases/ids-test.PNG "Post breach configuration")

## Assessing results

After running the Monkey, follow the Monkeys’ actions on the Monkey Island’s infection map.

Now you can match this activity from the Monkey timeline display to your internal SIEM and make sure your security
 solutions are identifying and correctly alerting on different attacks.

- The red arrows indicate successful exploitations. If you see red arrows, those incidents ought to be reported as
 exploitation attempts, so check whether you are receiving alerts from your security systems as expected.
- The orange arrows indicate scanning activity, usually used by attackers to locate potential vulnerabilities.
 If you see orange arrows, those incidents ought to be reported as scanning attempts (and possibly as segmentation violations).
- The blue arrows indicate tunneling activity, usually used by attackers to infiltrate “protected” networks from
 the Internet. Perhaps someone is trying to bypass your firewall to gain access to a protected service in your network?
 Check if your micro-segmentation / firewall solution identify or report anything.

While running this scenario, be on the lookout for the action that should arise:
 Did you get a phone call telling you about suspicious activity inside your network? Are events flowing
 into your security events aggregators? Are you getting emails from your IR teams?
 Is the endpoint protection software you installed on machines in the network reporting on anything? Are your
 compliance scanners detecting anything wrong?
 
Lastly, check Zero Trust and Mitre ATT&CK reports, to see which attacks can be executed on the network and how to
 fix it.
 
 ![Map](/images/usage/use-cases/map-full-cropped.png "Map")

