---
title: "Azure"
date: 2020-05-26T20:57:39+03:00
draft: false
pre: '<i class="fab fa-microsoft"></i> '
weight: 6
tags: ["setup", "azure"]
---

## Deployment

Select the [Infection Monkey from the Azure Marketplace](https://azuremarketplace.microsoft.com/en-us/marketplace/apps/guardicore.infection_monkey) and click **GET IT NOW**.

1. Under **Basics**:
    1. Choose a name for the new Infection Monkey instance, such as InfectionMonkey.
    1. Choose a username and password, or provide an SSH public key for authentication.
    1. Choose a resource group and the location for the Infection Monkey instance.
1. Under **Size**
    1. Choose a machine size with at least 1GB of RAM for optimal performance.
1. Under **Settings**
    1. Choose the network for the new instance.
    1. In the **Network Security Group** field, make sure port 5000 on the machine is accessible for inbound TCP traffic.
1. Under **Summary**
    1. Review the details of the offer and click **Create**.

At this point, Azure will provision and deploy your new machine. When ready,
you can browse to the Infection Monkey running on your fresh deployment at:

`https://{public-ip-address}:5000`

Once you have access to the Monkey Island server, check out the [getting started page]({{< ref "/usage/getting-started" >}}).

## Upgrading

Currently, there's no "upgrade-in-place" option when a new version is released.
To get the updated version, you can deploy a new machine from the marketplace.

If you'd like to keep your existing configuration, you can export it to a file
using the *Export config* button and then import it to the new Monkey Island.

![Import/export configuration](../../images/island/configuration_page/import_export_configuration.png "Import/export configuration")
