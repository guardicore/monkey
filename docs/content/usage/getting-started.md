---
title: "Getting Started"
date: 2020-05-26T21:01:12+03:00
draft: false
weight: 1
pre: "<i class='fas fa-play-circle'></i> "
tags: ["usage"]
---


<!-- TODO: Update screenshots -->

If you haven't deployed the Monkey Island yet, please [refer to our setup documentation](/setup).

## Using the Infection Monkey

After deploying the Monkey Island in your environment, navigate to `https://<server-ip>:5000`.

### First-time login

On your first login, you'll be asked to create a username and password for the Monkey Island server. [See this page for more details](../../setup/accounts-and-security).

### Running the Infection Monkey

To get the Infection Monkey running as fast as possible, click **Run Monkey**. Optionally, you can configure the Infection Monkey before you continue by clicking on **Configuration** (see [how to configure the Infection Monkey](../configuration)).

To run the Infection Monkey, select one of the following options:

![Run Page](/images/usage/getting-started/run_page_with_arrows.jpg "Run Page")

1. Click **Run on C&C Server** to run the Infection Monkey on the Monkey Island server. This simulates an attacker trying to propagate through your local network from the Monkey Island machine.
2. Click **Run on machine of your choice**  to download and execute the Infection Monkey on a machine of your choice. Then follow the instructions and run the generated command on the machine you selected. This simulates an attacker who has breached one of your servers. The Infection Monkey will map all accessible machines and their open services, attempting to steal credentials and use exploits to propagate.

![Run on machine of your choice](/images/usage/getting-started/run_page_button_no_arrow.jpg "Run on machine of your choice")

{{% notice tip %}}
If you're running the Infection Monkey in an AWS cloud environment, check out [Usage -> Integrations](../../usage/integrations) for information about how it integrates with AWS.
{{% /notice %}}

### Infection map

Next, click **Infection Map** to see the Infection Monkey in action.

![Run page to infection map page](/images/usage/getting-started/run_page_button.JPG "Run page to infection map page")

At first, the infection map will look like this:

![Start of Monkey execution](/images/usage/getting-started/run_island.JPG "Start of Monkey execution")

Within a few minutes, the Infection Monkey should be able to find and attack accessible machines.

![Middle of Monkey execution](/images/usage/getting-started/single_exploitation.JPG "Middle of Monkey execution")

As the simulation continues, the Infection Monkey will fill in the map with data on accessible and "hacked" machines. Once all the Infection Monkeys have finished propagating, click **Reports** to see the reports. See [Infection Monkey Reports](../reports) for more info.

![End of Monkey execution](/images/usage/getting-started/exploitation_tunneling_arrow.jpg "End of Monkey execution")

Congratulations, you finished your first successful execution of the Infection Monkey 🎉 ! To thoroughly test your network, you can run the Infection Monkey from different starting locations and use different configurations.
