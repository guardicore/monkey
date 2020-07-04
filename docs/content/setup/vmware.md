---
title: "VMware"
date: 2020-05-26T20:57:14+03:00
draft: false
pre: '<i class="fas fa-laptop-code"></i> '
weight: 3
tags: ["setup", "vmware"] 
---

## Deployment

1. Deploy the Infection Monkey OVA by choosing Deploy OVF Template and follow the wizard instructions. *Note: make sure port 5000 and 5001 on the machine are accessible for inbound TCP traffic.*
2. Turn on the Infection Monkey VM.
3. Log in to the machine with the following credentials:
   1. Username: **monkeyuser**
   2. Password: **Noon.Earth.Always**
4. It's recommended to change the machine passwords by running the following commands: `sudo passwd monkeyuser`, `sudo passwd root`.

## OVA network modes

The OVA can be used in one of two modes:

1. In a network with DHCP configured. In this case, the Monkey Island will automatically query and receive an IP address from the network.
1. With a static IP address.

    In this case, you should login to the VM console with
username `root` and password `G3aJ9szrvkxTmfAG`. After logging in, edit the interfaces file. You can do that by writing the following command in the prompt:

    ```sh
    sudo nano /etc/network/interfaces
    ```

    And change the lines:

    ```sh
    auto ens160
    iface ens160 inet dhcp
    ```

    to the following:

    ```sh
    auto ens160
    iface ens160 inet static
    address AAA.BBB.CCC.DDD
    netmask XXX.XXX.XXX.XXX
    gateway YYY.YYY.YYY.YYY
    ```

    Save the changes then run the command

    ```sh
    sudo ifdown ens160 && ifup ens160
    ```

## Upgrading

There's no "upgrade-in-place" option for Docker. To get the new version, download it, stop the current container, and run the installation commands again with the new file.

If you'd like to keep your existing configuration, you can export it to a file by using the Export button and then import it to the new server.

![Export configuration](../../images/setup/export-configuration.png "Export configuration")
