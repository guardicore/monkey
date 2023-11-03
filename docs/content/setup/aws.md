---
title: "AWS"
date: 2020-05-26T20:57:36+03:00
draft: false
pre: '<i class="fab fa-aws"></i> '
weight: 5
tags: ["setup", "aws"]
---

## Deployment

On the [Infection Monkey's AWS Marketplace page](https://aws.amazon.com/marketplace/pp/GuardiCore-Infection-Monkey/B07B3J7K6D), click **Continue to Subscribe**.

1. Choose the desired region.
1. Choose an EC2 instance type with at least 1GB of RAM for optimal performance or stick with the default recommendation.
1. Select the VPC and subnet you want to use for the new instance.
1. In the Security Group section, make sure port 5000 on the machine is accessible for inbound TCP traffic.
1. Choose an existing EC2 key pair for authenticating with the new instance.
1. Click **Launch with 1-click.**

At this point, AWS will instance and deploy the new machine.

When ready, you can browse to the Infection Monkey running on the fresh deployment at:

`https://{public-ip}`

To login to the machine, use *ubuntu* username.

Once you have access to the Monkey Island server, check out the [getting started page]({{< ref "/usage/getting-started" >}}).

## Configuration

Azure VM is running the AppImage deployment of the Infection Monkey. To configure the VM, shell
into it and follow configuration instructions in the [Linux setup section]({{< ref "/setup/linux#configuring-the-server" >}}).

## Integration with AWS services

The Infection Monkey has built-in integrations with AWS that allows running Agents on EC2 instances.
See [Usage -> Integrations](../../usage/integrations) for more details.

## Upgrading

Currently, there's no "upgrade-in-place" option when a new version is released.
To get an updated version, you can deploy a new machine from the marketplace.

If you'd like to keep your existing configuration, you can export it to a file
using the *Export config* button and then import it to the new Monkey Island.

![Import/export configuration](../../images/island/configuration_page/import_export_configuration.png "Import/export configuration")
