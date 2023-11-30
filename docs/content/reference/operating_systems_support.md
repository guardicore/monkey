---
title: "Operating systems"
date: 2020-07-14T08:09:53+03:00
draft: false
pre: '<i class="fas fa-laptop"></i> '
weight: 10
tags: ["setup", "reference", "windows", "linux"]
---

The Infection Monkey project supports many popular operating systems.

The Agent has wider support than the Monkey Island (control server) to make sure that users can
test even their legacy systems' security.

{{% notice info %}}
Infection Monkey only supports x86_64 (64-bit) systems.
{{% /notice %}}

### Agent support

#### Linux

Compatibility depends on GLIBC version (2.23+)[^1]. By default, these
distributions have been tested:

- CentOS/Rocky/RHEL 8+
- Debian 9+
- Kali 2019+
- openSUSE 15+
- Ubuntu 16+

#### Windows

- Windows 2012+
- Windows 2012_R2+
- Windows 7/Server 2008_R2 if [KB2999226](https://support.microsoft.com/en-us/help/2999226/update-for-universal-c-runtime-in-windows) is installed.
- Windows Vista/Server 2008 should also work if the same update is installed, but this wasn't tested.

### Server support

**The Monkey Island (control server)** runs out of the box on:

- Most modern Linux distros (see the [linux setup page]({{< ref "/setup/linux"
  >}}) for more details)
- Windows Server 2016
- Windows Server 2019
- Windows 10

We also provide a Dockerfile on Docker Hub. You can get it with `sudo docker
pull infectionmonkey/monkey-island:latest`.

[^1]: The GLIBC >= 2.23 requirement exists because the Infection Monkey Agent
  was built using this GLIBC version, and GLIBC is not backward compatible. We
  are also limited to the oldest GLIBC version compatible with Python 3.11.
