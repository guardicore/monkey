---
title: "Getting Started"
date: 2020-05-26T21:01:12+03:00
draft: false
weight: 1
---

## Using the Infection Monkey

After deploying the Monkey Island in your environment, navigate to `https://<server-ip>:5000`.

### First-time setup

On your first login, you'll be asked to set up a username and password for the Monkey Island server. [See this page for more details](../accounts-and-security).

### Run the Monkey

To get the Infection Monkey running as fast as possible, click **Run Monkey**. Optionally, you can configure the Monkey before you continue by clicking **Configuration** (see [how to configure the monkey](../configuration)).

- [ ] TODO put screenshot

To run the monkey, select one of the following options:

1. Click **Run on C&C Server** to run the Infection Monkey on the Monkey Island server. This simulates an attacker trying to propagate from a machine in the Monkey Island subnet.
1. Click **Run on machine of your choice** to download and execute the Infection Monkey on a machine of your choice. Then follow the instructions and execute the generated command on the machine of your choice. This simulates an attacker who has breached one of your servers. The Monkey will map all accessible machines and their open services and try to steal credentials and use its exploits to propagate.

- [ ] TODO put screenshot

### Infection Map

Next, click **Infection Map** to see the Infection Monkey in action.

- [ ] TODO put screenshot

At first, the infection map will look like this:

- [ ] TODO put screenshot

Within a few minutes, the Infection Monkey should be able to find and attack accessible machines.

- [ ] TODO put screenshot

As the Infection Monkey continues, the map should be filled with accessible and “hacked” machines. Once all the Infection Monkeys have finished propagating, click **Reports** (see [Infection Monkey Reports](../reports)) to see the reports.

- [ ] TODO put screenshot

Congratulations, you finished first successful execution of the Infection Monkey! 🎉 To thoroughly test your network, you can run the Infection Monkey from different starting locations using different configurations.
