---
title: "Infection Monkey Documentation"
draft: false
---

# Infection Monkey documentation


![Infection Monkey Documentation Logo](/images/monkey-teacher.svg?height=300px
"Infection Monkey Documentation Logo")

## What is Guardicore Infection Monkey?
Infection Monkey is an open-source adversary emulation platform that helps you
improve your security posture using empirical data. The Monkey uses various
methods to self-propagate across a network and reports its activities to a
centralized command and control server known as the Monkey Island. 🐵🏝️ You
know, like malware, but ✨safe.✨

## How does it work?

Infection Monkey is comprised of two components:

* **Agent** - A configurable network worm that can infect machines, steal
  data, and deliver payloads.
* **Monkey Island** - A command and control server used to control and
  visualize the Infection Monkey's progress throughout the simulation.

### Build up your malware antibodies 💉

![Malware Vaccine](/images/monkey-iv.png "Malware Vaccine")

You can think of Infection Monkey as a kind of "malware vaccine." Prior to the
invention of mRNA vaccines, biological vaccines worked as follows:

1. Collect a sample of the virus.
2. Through the magic of chemistry, create a weakened or inert form of the
   virus.
3. Inject the weakened virus into the human body, allowing the immune system to
   build up a defense.

Once the immune system has built up a defense, it can recognize and fight off
the real pathogen if it should ever infect the body.

**Infection Monkey aims to use this same approach to combat computer viruses
(or other types of malware.)**

1. Collect a sample of the malware.
2. Analyze the malware and understand its behaviors.
3. Modify Infection Monkey's configuration to enable behaviors that closely
   mimic those of the malware, but without causing damage to the target
   systems.
4. Inject the Monkey Agent into the network and validate (empirically) that
   your security controls can detect, prevent, or otherwise mitigate the
   infection.
5. If the infection is not successfully thwarted, take the necessary steps to
   "build up your immune response" by improving your security tools, policies,
   and processes.

Sun Tzu said, "if you know others and know yourself, you will not be imperiled
in a hundred battles." Knowledge of both your adversary's tactics and your own
defensive capabilities is necessary in order to successfully secure a network.
Infection Monkey aims helps you to know both.

Be the chimpion of your network. Learn more about the Monkey at
[akamai.com/infectionmonkey](https://www.akamai.com/infectionmonkey).


## Results

The results of running Monkey Agents are:
 - A map which displays how much of the network an attacker can see, what
   services are accessible and potential propagation routes.
 - A report, which displays security issues that Monkey Agents
   discovered and/or exploited.

A more in-depth description of reports generated can be found in the
[reports documentation page.](/features/reports)

### Infection Map
![Infection Map](/images/island/infection-map-page/infection-map.png "Infection Map")

### Security Report
![Security Report](/images/island/reports-page/security-report-overview.png "Security Report")

## Getting Started

If you're completely new to Infection Monkey, you can work through the
[tutorials](/tutorials/) to get your feet wet.

If you'd like to learn about Infection Monkey's capabilities, you can read
about its [features](/features/) and [use cases](/usage).

If you have a basic understanding of Infection Monkey, you can download it
[from our download page](https://github.com/guardicore/monkey/releases/latest).
After downloading the Monkey, install it using one of our
[setup guides,](/setup) and read our
[getting started guide!](/usage/getting-started)

## Support and community

If you need help or want to talk all things Monkey, you can [join our public
Slack
workspace](https://join.slack.com/t/infectionmonkey/shared_invite/zt-2cm5qiayf-yiEg5RPau0zQhki9xTlORA)
or [contact us via Email](mailto:support@infectionmonkey.com).
