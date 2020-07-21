---
title: "Operating systems"
date: 2020-07-14T08:09:53+03:00
draft: false
pre: '<i class="fas fa-laptop"></i> '
weight: 10
tags: ["setup", "reference", "windows", "linux"] 
---

The Infection Monkey project supports many popular OSes (but we can always do more).

The Monkey itself (the agent) has been tested to run on the following operating systems (on x64 architecture)

### Monkey support

#### Linux

Compatibility depends on GLIBC version (2.14+)[^1]. By default these distributions are supported:

- Centos 7+
- Debian 7+
- Kali 2019+
- Oracle 7+
- Rhel 7+
- Suse 12+
- Ubuntu 14+

#### Windows

- Windows 2012+
- Windows 2012_R2+
- Windows 7/Server 2008_R2 if [KB2999226](https://support.microsoft.com/en-us/help/2999226/update-for-universal-c-runtime-in-windows) is installed.
- Windows vista/Server 2008 should also work if the same update is installed, but this wasn't tested.

### Island support

**The Monkey Island (control server)** runs out of the box on:

- Ubuntu 18.04
- Debian 9
- Windows Server 2012
- Windows Server 2012 R2
- Windows Server 2016

We provide a dockerfile from our [website](http://infectionmonkey.com/) that lets the Monkey Island run inside a container.

### Old machine bootloader

Some **Older machines** still get a partial compatibility as in they get exploited and reported, but monkey can't run on them. So instead of monkey, old machine bootloader (small c program) is ran, which reports some minor info like network interface configuration, GLIBC version, OS and so on.

**Old machine bootloader** also has a GLIBC 2.14+ requirement for linux, because bootloader is included into pyinstaller bootloader which uses python3.7, which in turn requires GLIBC 2.14+. If you think partial support for older machines is important, don't hesitate to open a new issue about it.

**Old machine bootloader** runs on machines with:

- Centos 7+
- Debian 7+
- Kali 2019+
- Oracle 7+
- Rhel 7+
- Suse 12+
- Ubuntu 14+
- **Windows XP/Server 2003+**

[^1]: GLIBC >= 2.14 requirement comes from the fact that monkey is built using this GLIBC version and GLIBC is not backwards compatible. We are also limited to the oldest GLIBC version compatible with ptyhon3.7
