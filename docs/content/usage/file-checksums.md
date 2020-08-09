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
infection_monkey_deb.tgz | Debian Package | 1.9.0 | `33c23ddae283e3aafe965d264bc88464b66db3dd6874fd7e5cbcd4e931b3bb25`
infection_monkey_debzt.tgz | Debian Package | 1.9.0 | `cc53fe9632f44248357d6bd20cf8629be9baf8688468fa6d3e186dcebf10cef6`
Monkey Island v1.9.0_3546_windows.exe | Windows Installer | 1.9.0 | `371f6d25e8cb16ea7ebdfd367092ee65b33db2ec35b44d96705716641eaa59e8`
Monkey Island v1.9.0_3546_windowszt.exe | Windows Installer | 1.9.0 | `662c611fb83bb8c7ef5f99c5d5ae04f5758727c688238d6a3cd4c58675581695`
infection_monkey_docker_docker_20200806_153913.tgz | Docker | 1.9.0 | `5da11c539045a395ced5dd572d331c4f0e9315a3ee192c06279ff4fef668b96e`
infection_monkey_docker_dockerzt_20200806_154742.tgz | Docker | 1.9.0 | `a84dbaad32ae42cc2d359ffbe062aec493a7253cf706a2d45f0d0b1c230f9348`
monkey-island-vmware.ova | OVA | 1.9.0 | `3861d46518e8a92e49992b26dbff9fe8e8a4ac5fd24d68e68b13e7fd3fa22247`
monkey-island-vmwarezt.ova | OVA | 1.9.0 | `03d356eb35e6515146f5bd798bb62cb15c56fcdf83a5281cf6cdc9b901586026`


## Older checksums

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
monkey-windows-64.exe | Windows Agent | 1.8.0 | `f0bc144ba4ff46094225adaf70d3e92e9aaddb13b59e4e47aa3c2b26fd7d9ad7`
monkey-windows-32.exe | Windows Agent | 1.8.0 | `1ddb093f9088a4d4c0af289ff568bbe7a0d057e725e6447055d4fe6c5f4e2c08`
monkey-linux-64 | Linux Agent | 1.8.0 | `d41314e5df72d5a470974522935c0b03dcb1c1e6b094d4ab700b04d5fec59ae6`
monkey-linux-32 | Linux Agent | 1.8.0 | `217cc2b9481f6454fa0a13adf12d9b29ce4e1e6a319971c8db9b446952ce3fb2`
infection_monkey_deb.tgz | Debian Package | 1.8.0 | `9c5254583ce786768ea55df8063152bd19e0f21a83e6f4f873c5dccc5a1c9d5e`
infection_monkey_debzt.tgz | Debian Package | 1.8.0 | `90A0824EC98680944B15B86CF5CFA09D48EDA406300C4CAE54432DB05F486D07`
Monkey Island v1.8.0_3513_windows.exe | Windows Installer | 1.8.0 | `ce9a9d0539c14ebe2a10cf3b36991b309abd7b62dd7fb7522a549d8987b0f0f4`
Monkey Island v1.8.0_3514_windowszt.exe | Windows Installer | 1.8.0 | `0b535a802ac43455d702b45673859b940c1feb7702b46a6a2cbc699672b0c89d`
infection_monkey_docker_docker_20200330_201419.tgz | Docker | 1.8.0 | `4f15a5008e43d8c5184456771dd9e8d70104b4ec79e34b53d230662604a7d190`
infection_monkey_docker_dockerzt_20200401_174529.tgz | Docker | 1.8.0 | `d94404134d879f3d859c77454df4abd0dbca00b8cae4b1c52d3b38e847f34e4c`
monkey-island-vmware.ova | OVA | 1.8.0 | `6BC4E85A0EA81045BD88E2D5A9F98F0DD40DE99E94D1E343D13FA418045A6915`
monkey-island-vmwarezt.ova | OVA | 1.8.0 | `79A043D85521F94024F8B0428A7A33B4D3F5B13F9D2B83F72C73C8D0BB12ED91`
