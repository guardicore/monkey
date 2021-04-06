---
title: "VMware"
date: 2020-05-26T20:57:14+03:00
draft: false
pre: '<i class="fas fa-laptop-code"></i> '
weight: 3
tags: ["setup", "vmware"]
---

## Deployment

1. Deploy the Infection Monkey OVA by choosing **Deploy OVF Template** and
   following the wizard instructions. *Note: make sure ports 5000 and 5001 on
   the machine are accessible for inbound TCP traffic.*
1. Turn on the Infection Monkey VM.
1. Log in to the machine with the following credentials:
   1. Username: **monkeyuser**
   1. Password: **Noon.Earth.Always**
1. For security purposes, it's recommended that you change the machine
   passwords by running the following commands: `sudo passwd monkeyuser`, `sudo
   passwd root`.

## OVA network modes

You can use the OVA in one of two modes:

1. In a network with the DHCP configured — In this case, the Monkey Island will
   automatically query and receive an IP address from the network.
1. With a static IP address — In this case, you should log in to the VM console
   with the username `monkeyuser` and the password `Noon.Earth.Always`. After logging
   in, edit the Netplan configuration by entering the following command in the
   prompt:

    ```sh
    sudo nano /etc/netplan/00-installer-config.yaml
    ```

    Make the following changes:

    ```diff
     # This is the network config written by 'subiquity'
     network:
       ethernets:
         ens160:
    -      dhcp4: true
    +      dhcp4: false
    +      addresses: [XXX.XXX.XXX.XXX/24]
    +      gateway4: YYY.YYY.YYY.YYY
    +      nameservers:
    +        addresses: [1.1.1.1]
       version: 2
    ```

    Replace `XXX.XXX.XXX.XXX` with the desired IP addess of the VM. Replace
    `YYY.YYY.YYY.YYY` with the default gateway.

    Save the changes then run the command:

    ```sh
    sudo netplan apply
    ```

    If this configuration does not suit your needs, see
    https://netplan.io/examples/ for more information about how to configure
    Netplan.

## Upgrading

Currently, there's no "upgrade-in-place" option when a new version is released.
To get an updated version, download the updated OVA file.

If you'd like to keep your existing configuration, you can export it to a file
using the *Export config* button and then import it to the new Monkey Island.

![Export configuration](../../images/setup/export-configuration.png "Export configuration")
