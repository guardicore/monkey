+++
title = "Contribute"
date = 2020-05-26T20:55:04+03:00
weight = 30
chapter = true
pre = '<i class="fas fa-code"></i> '
tags = ["development", "contribute"]
+++

# Securing networks together

Want to help secure networks? That's great!

{{% notice warning %}}
The Infection Monkey project is currently undergoing major changes. Some of the
information here may be outdated and will be updated soon.
{{% /notice %}}

## How should I start?

Here are a few short links to help you get started:

* [Getting up and running]({{< ref "/development/setup-development-environment" >}}) - These instructions will help you get a working development setup.
* [Contributing guidelines](https://github.com/guardicore/monkey/blob/master/CONTRIBUTING.md) - These guidelines will help you submit.

## What are we looking for?

You can take a look at [our roadmap](https://github.com/guardicore/monkey/projects/5) to see what issues we're thinking about tackling soon. We are always looking for:

### More exploits! 💥

The best way to find weak spots in a network is by attacking it.

It's important to note that the Infection Monkey must be absolutely reliable. Otherwise, no one will use it, so avoid memory corruption exploits unless they're rock solid and focus on the logical vulns such as Hadoop.

### Analysis plugins 🔬

Successfully attacking every server in the network has little value if the Infection Monkey cannot provide recommendations for reducing future risk. Whether it's explaining how the Infection Monkey used stolen credentials or escaped from locked-down networks, analysis is what helps users translate the Infection Monkey's activities into actionable next steps for improving security.

### Better code 💪

We always want to improve the core Infection Monkey code to make it smaller, faster and more reliable. Please share if you have an idea that will help us meet these goals or modularize/improve test coverage.

### Documentation 📚

Every project requires excellent documentation. The Infection Monkey is no different. Please feel free to open pull requests with suggestions, improvements or issues and ask us to document various parts of the Monkey.

The Infection Monkey's documentation is stored in the `/docs/content` directory.
