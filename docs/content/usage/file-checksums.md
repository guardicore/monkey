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
monkey-windows-64.exe | Windows Agent | 1.9.0 | `24622cb8dbabb0cf4b25ecd3c13800c72ec5b59b76895b737ece509640d4c068`
monkey-windows-32.exe | Windows Agent | 1.9.0 | `67f12171c3859a21fc8f54c5b2299790985453e9ac028bb80efc7328927be3d8`
monkey-linux-64 | Linux Agent | 1.9.0 | `aec6b14dc2bea694eb01b517cca70477deeb695f39d40b1d9e5ce02a8075c956`
monkey-linux-32 | Linux Agent | 1.9.0 | `4c24318026239530ed2437bfef1a01147bb1f3479696eb4eee6009326ce6b380`
infection_monkey_deb.tgz | Debian Package | 1.9.0 | `8dff2e5995ff889f97ef3d4bcb51d80b63384b45e51bc76ed655df08bde51e06`
Monkey Island v1.9.0_3545_windows.exe | Windows Installer | 1.9.0 | `8eb9791e9294b94a62f94e6fdb4072425f6012cd8df24df58902deb79dff59e3`
Monkey Island v1.9.0_3545_windowszt.exe | Windows Installer | 1.9.0 | `da5f08fa229e79e9ca1537c6e7ce70e26efcac9123fdb00cfeed41109c7e60de`
infection_monkey_docker_docker_20200805_231255.tgz | Docker | 1.9.0 | `408e100e340cb8a6b78ec51bb46b07c484f3980d38ba428231f1df50c3d85f87`
infection_monkey_docker_dockerzt_20200805_231705.tgz | Docker | 1.9.0 | `c1edbd534730c519fec7645908cb4564aa4115c5c8b41a48c741cddbd596c3e4`

## All checksums

### 1.8.0 and older

You can find all these checksums in [this page](https://www.guardicore.com/infectionmonkey/checksums.html).
