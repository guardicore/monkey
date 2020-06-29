---
title: "Verify Integrity - Checksums"
date: 2020-06-08T19:53:47+03:00
draft: false
weight: 100
pre: "<i class='fas fa-certificate'></i> "
---

The official distribution of Infection Monkey is compiled and supplied by Guardicore ([download from our official site here](https://www.guardicore.com/infectionmonkey/#download)). The team signs all software packages to certify that a particular Infection Monkey package is a valid and unaltered Infection Monkey release. Before installing Monkey, you should validate the package using the SHA-256 checksum.

## How to get SHA-256 checksum

### On Windows

Use the `Get-FileHash` <i class="fas fa-terminal"></i> PowerShell commandlet, like so:

```powershell
Get-FileHash '.\Monkey Island v1.8.2_3536_windows.exe' | Format-List

# Should print
#   Algorithm : SHA256
#   Hash      : 2BE528685D675C882604D98382ADB739F5BA0A7E234E3569B21F535173BD9569
#   Path      : C:\Users\shay.nehmad\Desktop\work\compiled monkeys\1.8.2\Monkey Island v1.8.2_3536_windows.exe
```

### On Linux

Use the `sha256sum` <i class="fas fa-terminal"></i> shell command, like so:

```sh
sha256sum monkey-linux-64
# Should print:
#   734dd2580f3d483210daf54c063a0a972911bbe9afb6ebc6278f86cd6b05e7ab  monkey-linux-64
```

## Latest version checksums

| Filename | Type | Version | SHA256 hash |
|-|-|-|-|
monkey-windows-64.exe | Windows Agent | 1.8.2 | `2e6a1cb5523d87ddfd48f75b10114617343fbac8125fa950ba7f00289b38b550`
monkey-windows-32.exe | Windows Agent | 1.8.2 | `86a7d7065e73b795e38f2033be0c53f3ac808cc67478aed794a7a6c89123979f`
monkey-linux-64 | Linux Agent | 1.8.2 | `4dce4a115d41b43adffc11672fae2164265f8902267f1355d02bebb802bd45c5`
monkey-linux-32 | Linux Agent | 1.8.2 | `39d3fe1c7b33482a8cb9288d323dde17b539825ab2d736be66a9582764185478`
infection_monkey_deb.tgz | Debian Package | 1.8.2 | `2a6b4b9b846566724ff985c6cc8283222b981b3495dd5a8920b6bc3f34d556e2`
Monkey Island v1.8.2_3536_windows.exe | Windows Installer | 1.8.2 | `2be528685d675c882604d98382adb739f5ba0a7e234e3569b21f535173bd9569`
Monkey Island v1.8.2_3536_windowszt.exe | Windows Installer | 1.8.2 | `f282ce4dd50abe54671948fb5b3baf913087459444e451660971290a72fe244a`
infection_monkey_docker_docker_20200607_172156.tgz | Docker | 1.8.2 | `0e4bc731ef7e8bf19b759709672375890136c008526be454850d334d9ba5012d`
infection_monkey_docker_dockerzt_20200607_172521.tgz | Docker | 1.8.2 | `0f4b0cd6fd54dc14ea50c5d2fb3fc711e9863518bd5bffd04e08a0f17eb99e75`

## All checksums

### 1.8.0 and older

You can find all these checksums in [this page](https://www.guardicore.com/infectionmonkey/checksums.html).
