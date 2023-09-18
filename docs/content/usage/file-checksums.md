---
title: "Verify Integrity - Checksums"
date: 2020-06-08T19:53:47+03:00
draft: false
weight: 100
pre: "<i class='fas fa-certificate'></i> "
---

The official distribution of Infection Monkey is compiled and supplied by Guardicore ([download from our official site here](https://www.akamai.com/infectionmonkey#download)). The team signs all software packages to certify that a particular Infection Monkey package is a valid and unaltered Infection Monkey release. Before installing Infection Monkey, you should validate the package using the SHA-256 checksum.

## How to get SHA-256 checksum

### On Windows

Use the `Get-FileHash` <i class="fas fa-terminal"></i> PowerShell commandlet, like so:

```powershell
Get-FileHash '<FILE_NAME>' | Format-List
```

### On Linux

Use the `sha256sum` <i class="fas fa-terminal"></i> shell command, like so:

```sh
$ sha256sum <FILE_NAME>
```

## Latest version checksums

| Filename                                             | Type              | Version | SHA256                                                             |
|------------------------------------------------------|-------------------|---------|--------------------------------------------------------------------|
| monkey-linux-64                                      | Linux Agent       | 2.3.0   | `ca72ee64ab6f44bbf885a33a4a7b9848a524d7c46407ec71c8ec7b5c88e49eac` |
| monkey-windows-64.exe                                | Windows Agent     | 2.3.0   | `c189438c9a07d40dac0bd3ed8f5050ce3f05abe47df425a47c1250be9c8b8479` |
| InfectionMonkey-docker-v2.3.0.tgz                    | Docker            | 2.3.0   | `53d52879d72a4e2e164e68e5c587345182af6d3f997b30585af5ec85f34421e2` |
| InfectionMonkey-v2.3.0.AppImage                      | Linux Package     | 2.3.0   | `d4a33ed23a710cadc13d0d5b7c53b4b25e4d7ca32e3d9d051e339990b81eb7be` |
| InfectionMonkey-v2.3.0.exe                           | Windows Installer | 2.3.0   | `8c66d86af64d0f922bc369a1d4f044c9da31f15553711fe53ff889163f996d3c` |


## Older checksums

| Filename                                             | Type              | Version | SHA256                                                             |
|------------------------------------------------------|-------------------|---------|--------------------------------------------------------------------|
| monkey-linux-64                                      | Linux Agent       | 2.2.1   | `333a9f5c32780aa32e822f95801a13263015afd3fa11d5e5b1c4fb0af30279fc` |
| monkey-windows-64.exe                                | Windows Agent     | 2.2.1   | `d49b233a31f808af4786b8cedd3772f8b79f28fe726915387542d5c8bed2fafc` |
| InfectionMonkey-docker-v2.2.1.tgz                    | Docker            | 2.2.1   | `21f84970ef69d21d779c43046a475cd8acefaaf16836f801d5c4c4ca987f86e8` |
| InfectionMonkey-v2.2.1.AppImage                      | Linux Package     | 2.2.1   | `cc9af5fe29cd978bbecafe454c9d722921870361fd1351c2447681b4cbe1b4a4` |
| InfectionMonkey-v2.2.1.exe                           | Windows Installer | 2.2.1   | `74cd99dd087334ab7a87aafc5cc21faca48f32baa5bb38b51223434c548776b3` |
| monkey-windows-64.exe                                | Windows Agent     | 2.1.0   | `883b16c9f8d9a532da6787a1a088bef6fabba782058bcedbd1e02afc613b88c2` |
| monkey-linux-64                                      | Linux Agent       | 2.1.0   | `d7217665f714fbde6657f3b4ac60182779dfd2668fc9a308a77fc595be711252` |
| InfectionMonkey-v2.1.0.AppImage                      | Linux Package     | 2.1.0   | `a788e693d4e785e039aad513ebd626be1d265e961a2f44dc06df3c9eae33cd8e` |
| InfectionMonkey-docker-v2.1.0.tgz                    | Docker            | 2.1.0   | `d78c8bcc71988932c22b867f74ec71e5c5b99e204e959ad0fe55e7552a1b8928` |
| InfectionMonkey-v2.1.0.exe                           | Windows Installer | 2.1.0   | `62095752eee71776f050712670c42c57d2fa439ca5f842cb1ff0830e52b2bdc0` |
| monkey-windows-64.exe                                | Windows Agent     | 2.0.0   | `7d848e1cc4855b8476b27e81dfb01b4e38a2d0a421f80507b08a99ab7c71e4ea` |
| monkey-linux-64                                      | Linux Agent       | 2.0.0   | `07c8ed75f1a83ace2d018f4645b7a147c31075f41963a1d801e4e5133014189a` |
| InfectionMonkey-v2.0.0.AppImage                      | Linux Package     | 2.0.0   | `b40ffde3e55f2b2198e8f26c44a1beb33a84a0979764a47ffb5ce26f07f4fa8e` |
| InfectionMonkey-docker-v2.0.0.tgz                    | Docker            | 2.0.0   | `fa75631d6fa6d6d5086d936077e8005b8b7f59626c78ca561de80470ce5d42f0` |
| InfectionMonkey-v2.0.0.exe                           | Windows Installer | 2.0.0   | `bbe670cec5c16fbfbec63719594830a52f9495899f96a06fd5c587c6390c3269` |
| monkey-windows-64.exe                                | Windows Agent     | 1.13.0  | `3EDD20DE2247047C8A822C84145981936CE2FD0BDF843EB5CA777CA4D2478B35` |
| monkey-windows-32.exe                                | Windows Agent     | 1.13.0  | `7497907E3CF4FFEB121A7795BFA16709800E6E0F99770F64AF7FFF684ECBA6D6` |
| monkey-linux-64                                      | Linux Agent       | 1.13.0  | `F21E709CB7BA8DAF90B908AF5FE485BA43866C325D3C7CE1EB07E8A2323E07C1` |
| monkey-linux-32                                      | Linux Agent       | 1.13.0  | `24C5779825F26C76A8910794836647096F4BB4B47CFD6AD213CC48116D140FAB` |
| InfectionMonkey-v1.13.0.AppImage                     | Linux Package     | 1.13.0  | `CDED4E8394A4D2A809BA9B74B924AEA590317515B9B032BA8005A93DFCE1C861` |
| InfectionMonkey-docker-v1.13.0.tgz                   | Docker            | 1.13.0  | `342701BA8EC5B754C59685896FC3DCDBB93362FFFAD0EC7F9E2E5B99DA26F5EC` |
| InfectionMonkey-v1.13.0.exe                          | Windows Installer | 1.13.0  | `D35ED6CAF21AC786D9A438510282FA07AEF812590A5E6405A01F2B06661B33B9` |
| monkey-windows-64.exe                                | Windows Agent     | 1.12.0  | `02e5e051a96e2ca61ae8e661b3a5828ee53a0fc00aca6502d5c73a46754f0d07` |
| monkey-windows-32.exe                                | Windows Agent     | 1.12.0  | `3c10f610f47c4fd227cf85f6bf800d66ed31fe37dc2e2ed408860483685ba504` |
| monkey-linux-64                                      | Linux Agent       | 1.12.0  | `1ad52eabd704a9b0fbf642fa552629f30d3c5c27e431a687bd4cba4e0104d3f7` |
| monkey-linux-32                                      | Linux Agent       | 1.12.0  | `d941943046db48cf0eb7f11e144a79749848ae6b50014833c5390936e829f6c3` |
| InfectionMonkey-v1.12.0.AppImage                     | Linux Package     | 1.12.0  | `1325f2aa1d0c27aec2e2f9864ed53c53c524bd208313f87ea6606f59c90ff310` |
| InfectionMonkey-docker-v1.12.0.tgz                   | Docker            | 1.12.0  | `dcaf669411d55ea6883920597af4a35f3735a286801e08b6ef047cc91ff32769` |
| InfectionMonkey-v1.12.0.exe                          | Windows Installer | 1.12.0  | `4d6e0373be3615a4b97721a07d2a854f6316d1ce8c4ff6d6495aac3a8f2c6a69` |
| monkey-windows-64.exe                                | Windows Agent     | 1.11.0  | `12c55377381a8fc7d8ff731db52302ef2f8bb894d8712769e5a91a140ba22b0a` |
| monkey-windows-32.exe                                | Windows Agent     | 1.11.0  | `e006b26663f59b92bad8d49b034cd8101dd481f881e3c4839a9c1e64fd99e849` |
| monkey-linux-64                                      | Linux Agent       | 1.11.0  | `fb4c979ce6c29bb458be50a44cc6839650826b831da849da69a05dfefdc66462` |
| monkey-linux-32                                      | Linux Agent       | 1.11.0  | `88d6d717f99047ae6f8ff9527b41ff004217c99b1b027f112d062dd9e66d11ab` |
| Infection_Monkey-1.11.0-x86_64.AppImage              | Linux Package     | 1.11.0  | `6312b6bff18c11c7db694f42cf5a41e894786c39e3e093b6b15abcbff80337f2` |
| infection_monkey_docker_20210811_211212.tgz          | Docker            | 1.11.0  | `40f203387cadd153f97c6a21dfdddacd4d4eeea334a9300d862bfb4ba528e2e6` |
| Monkey Island v1.11.0_3789.exe                       | Windows Installer | 1.11.0  | `20633c1993ea5f86b57b3a48d6875e8f72881f856f4713d747f07a559da05ccc` |
| monkey-windows-64.exe                                | Windows Agent     | 1.10.0  | `3b499a4cf1a67a33a91c73b05884e4d6749e990e444fa1d2a3281af4db833fa1` |
| monkey-windows-32.exe                                | Windows Agent     | 1.10.0  | `8e891e90b11b97fbbef27f1408c1fcad486b19c612773f2d6a9edac5d4cdb47f` |
| monkey-linux-64                                      | Linux Agent       | 1.10.0  | `932f703510b6484c3824fc797f90f99722e38a7f8956cf6fa58fdecb3790ab93` |
| monkey-linux-32                                      | Linux Agent       | 1.10.0  | `a6de7d571051292b9db966afe025413dc20b214c4aab53e48d90d8e04264f4f5` |
| infection_monkey_deb.tgz                             | Debian Package    | 1.10.0  | `534d85c4abc78e2c86a74d8b88759b091b62077dd9e32f02eeb43d716d359ff6` |
| infection_monkey_debzt.tgz                           | Debian Package    | 1.10.0  | `bd01d8482f80990e6cc0ed654c07dbd80da71eebe3dd244365e9bc00f86b1c03` |
| Monkey Island v1.10.0_3593_windows.exe               | Windows Installer | 1.10.0  | `ebd2c5627d21dd8670def02c3a5a995f9e799ba567cf4caacd702654264ddf06` |
| Monkey Island v1.10.0_3593_windowszt.exe             | Windows Installer | 1.10.0  | `60aaf3b32e5d06c91fe0d4f1b950529517ac33796f67e9ccfef0e8ce1c5372d8` |
| infection_monkey_docker_docker_20210326_171631.tgz   | Docker            | 1.10.0  | `e4f9c7c5aafe7e38b33d2927a9c0cf6a3ac27858d3d0e3f2252c2e91809a78db` |
| infection_monkey_docker_dockerzt_20210326_172035.tgz | Docker            | 1.10.0  | `248640e9eaa18e4c27f67237f0594d9533732f372ba4674d5d1bea43ab498cf5` |
| monkey-island-vmware.ova                             | OVA               | 1.10.0  | `3472ad4ae557ddad7d7db8fbbfcfd33c4f2d95d870b18fa4cab49af6b562009c` |
| monkey-island-vmwarezt.ova                           | OVA               | 1.10.0  | `3472ad4ae557ddad7d7db8fbbfcfd33c4f2d95d870b18fa4cab49af6b562009c` |
| monkey-windows-64.exe                                | Windows Agent     | 1.9.0   | `24622cb8dbabb0cf4b25ecd3c13800c72ec5b59b76895b737ece509640d4c068` |
| monkey-windows-32.exe                                | Windows Agent     | 1.9.0   | `67f12171c3859a21fc8f54c5b2299790985453e9ac028bb80efc7328927be3d8` |
| monkey-linux-64                                      | Linux Agent       | 1.9.0   | `aec6b14dc2bea694eb01b517cca70477deeb695f39d40b1d9e5ce02a8075c956` |
| monkey-linux-32                                      | Linux Agent       | 1.9.0   | `4c24318026239530ed2437bfef1a01147bb1f3479696eb4eee6009326ce6b380` |
| infection_monkey_deb.tgz                             | Debian Package    | 1.9.0   | `33c23ddae283e3aafe965d264bc88464b66db3dd6874fd7e5cbcd4e931b3bb25` |
| infection_monkey_debzt.tgz                           | Debian Package    | 1.9.0   | `cc53fe9632f44248357d6bd20cf8629be9baf8688468fa6d3e186dcebf10cef6` |
| Monkey Island v1.9.0_3546_windows.exe                | Windows Installer | 1.9.0   | `371f6d25e8cb16ea7ebdfd367092ee65b33db2ec35b44d96705716641eaa59e8` |
| Monkey Island v1.9.0_3546_windowszt.exe              | Windows Installer | 1.9.0   | `662c611fb83bb8c7ef5f99c5d5ae04f5758727c688238d6a3cd4c58675581695` |
| infection_monkey_docker_docker_20200806_153913.tgz   | Docker            | 1.9.0   | `5da11c539045a395ced5dd572d331c4f0e9315a3ee192c06279ff4fef668b96e` |
| infection_monkey_docker_dockerzt_20200806_154742.tgz | Docker            | 1.9.0   | `a84dbaad32ae42cc2d359ffbe062aec493a7253cf706a2d45f0d0b1c230f9348` |
| monkey-island-vmware.ova                             | OVA               | 1.9.0   | `3861d46518e8a92e49992b26dbff9fe8e8a4ac5fd24d68e68b13e7fd3fa22247` |
| monkey-island-vmwarezt.ova                           | OVA               | 1.9.0   | `03d356eb35e6515146f5bd798bb62cb15c56fcdf83a5281cf6cdc9b901586026` |
| monkey-windows-64.exe                                | Windows Agent     | 1.8.2   | `2e6a1cb5523d87ddfd48f75b10114617343fbac8125fa950ba7f00289b38b550` |
| monkey-windows-32.exe                                | Windows Agent     | 1.8.2   | `86a7d7065e73b795e38f2033be0c53f3ac808cc67478aed794a7a6c89123979f` |
| monkey-linux-64                                      | Linux Agent       | 1.8.2   | `4dce4a115d41b43adffc11672fae2164265f8902267f1355d02bebb802bd45c5` |
| monkey-linux-32                                      | Linux Agent       | 1.8.2   | `39d3fe1c7b33482a8cb9288d323dde17b539825ab2d736be66a9582764185478` |
| infection_monkey_deb.tgz                             | Debian Package    | 1.8.2   | `2a6b4b9b846566724ff985c6cc8283222b981b3495dd5a8920b6bc3f34d556e2` |
| Monkey Island v1.8.2_3536_windows.exe                | Windows Installer | 1.8.2   | `2be528685d675c882604d98382adb739f5ba0a7e234e3569b21f535173bd9569` |
| Monkey Island v1.8.2_3536_windowszt.exe              | Windows Installer | 1.8.2   | `f282ce4dd50abe54671948fb5b3baf913087459444e451660971290a72fe244a` |
| infection_monkey_docker_docker_20200607_172156.tgz   | Docker            | 1.8.2   | `0e4bc731ef7e8bf19b759709672375890136c008526be454850d334d9ba5012d` |
| infection_monkey_docker_dockerzt_20200607_172521.tgz | Docker            | 1.8.2   | `0f4b0cd6fd54dc14ea50c5d2fb3fc711e9863518bd5bffd04e08a0f17eb99e75` |
| monkey-windows-64.exe                                | Windows Agent     | 1.8.0   | `f0bc144ba4ff46094225adaf70d3e92e9aaddb13b59e4e47aa3c2b26fd7d9ad7` |
| monkey-windows-32.exe                                | Windows Agent     | 1.8.0   | `1ddb093f9088a4d4c0af289ff568bbe7a0d057e725e6447055d4fe6c5f4e2c08` |
| monkey-linux-64                                      | Linux Agent       | 1.8.0   | `d41314e5df72d5a470974522935c0b03dcb1c1e6b094d4ab700b04d5fec59ae6` |
| monkey-linux-32                                      | Linux Agent       | 1.8.0   | `217cc2b9481f6454fa0a13adf12d9b29ce4e1e6a319971c8db9b446952ce3fb2` |
| infection_monkey_deb.tgz                             | Debian Package    | 1.8.0   | `9c5254583ce786768ea55df8063152bd19e0f21a83e6f4f873c5dccc5a1c9d5e` |
| infection_monkey_debzt.tgz                           | Debian Package    | 1.8.0   | `90A0824EC98680944B15B86CF5CFA09D48EDA406300C4CAE54432DB05F486D07` |
| Monkey Island v1.8.0_3513_windows.exe                | Windows Installer | 1.8.0   | `ce9a9d0539c14ebe2a10cf3b36991b309abd7b62dd7fb7522a549d8987b0f0f4` |
| Monkey Island v1.8.0_3514_windowszt.exe              | Windows Installer | 1.8.0   | `0b535a802ac43455d702b45673859b940c1feb7702b46a6a2cbc699672b0c89d` |
| infection_monkey_docker_docker_20200330_201419.tgz   | Docker            | 1.8.0   | `4f15a5008e43d8c5184456771dd9e8d70104b4ec79e34b53d230662604a7d190` |
| infection_monkey_docker_dockerzt_20200401_174529.tgz | Docker            | 1.8.0   | `d94404134d879f3d859c77454df4abd0dbca00b8cae4b1c52d3b38e847f34e4c` |
| monkey-island-vmware.ova                             | OVA               | 1.8.0   | `6BC4E85A0EA81045BD88E2D5A9F98F0DD40DE99E94D1E343D13FA418045A6915` |
| monkey-island-vmwarezt.ova                           | OVA               | 1.8.0   | `79A043D85521F94024F8B0428A7A33B4D3F5B13F9D2B83F72C73C8D0BB12ED91` |
| monkey-linux-64                                      | Debian Package    | 1.8.0   | `b0de3931f6b9c2d986860151e5094e4c57aafa5e3e4aced828ecba36e4ece851` |
| infection_monkey_docker_docker_20200330_201419.tgz   | Docker            | 1.8.0   | `4f15a5008e43d8c5184456771dd9e8d70104b4ec79e34b53d230662604a7d190` |
| Monkey Island v1.8.0_3513_windows.exe                | Windows Installer | 1.8.0   | `ce9a9d0539c14ebe2a10cf3b36991b309abd7b62dd7fb7522a549d8987b0f0f4` |
| monkey-windows-64.exe                                | Windows Agent     | 1.8.0   | `f0bc144ba4ff46094225adaf70d3e92e9aaddb13b59e4e47aa3c2b26fd7d9ad7` |
| monkey-linux-64                                      | Linux Agent       | 1.8.0   | `d41314e5df72d5a470974522935c0b03dcb1c1e6b094d4ab700b04d5fec59ae6` |
| monkey-windows-32.exe                                | Windows Agent     | 1.8.0   | `1ddb093f9088a4d4c0af289ff568bbe7a0d057e725e6447055d4fe6c5f4e2c08` |
| monkey-linux-32                                      | Linux Agent       | 1.8.0   | `217cc2b9481f6454fa0a13adf12d9b29ce4e1e6a319971c8db9b446952ce3fb2` |
| infection_monkey_deb.tgz                             | Debian Package    | 1.8.0   | `9c5254583ce786768ea55df8063152bd19e0f21a83e6f4f873c5dccc5a1c9d5e` |
| infection_monkey_debzt.tgz                           | Debian Package    | 1.8.0   | `90A0824EC98680944B15B86CF5CFA09D48EDA406300C4CAE54432DB05F486D07` |
| infection_monkey_docker_docker_20200401_174048.tgz   | Docker            | 1.8.0   | `ae59b222a94e1ec83a1c36917bc5cd3d119057e146ac01242af91808f3dce37a` |
| infection_monkey_docker_dockerzt_20200401_174529.tgz | Docker            | 1.8.0   | `d94404134d879f3d859c77454df4abd0dbca00b8cae4b1c52d3b38e847f34e4c` |
| Monkey Island v1.8.0_3514_windows.exe                | Windows Installer | 1.8.0   | `a56bd98ca3d0dd260f26ac5ee46022fd5ca3f9081a43535b4f57cef43c345dc0` |
| Monkey Island v1.8.0_3514_windowszt.exe              | Windows Installer | 1.8.0   | `0b535a802ac43455d702b45673859b940c1feb7702b46a6a2cbc699672b0c89d` |
| Monkey Island v1.8.0_3516_windows.exe                | Windows Installer | 1.8.0   | `a31a3837d8ca722e8db10148704237b032e5ef62acc080a82ab80f009d8de6bd` |
| Monkey Island v1.8.0_3517_windows.exe                | Windows Installer | 1.8.0   | `450e9ea58a5282f506f819bdc3d4477bbc917d74ee837ca0cc3e62b4a923fef1` |
| Monkey Island v1.8.0_3519_windows.exe                | Windows Installer | 1.8.0   | `dfaf7b11b148a5648ca92887d731633f85b68dc82313616f0009eee123c47352` |
| Monkey Island v1.8.0_3520_windows.exe                | Windows Installer | 1.8.0   | `719427a7f1878555d6940485330f51e2ddb3331c96b60a1719f6e21987efb3d3` |
| Monkey Island v1.8.0_3521_windows.exe                | Windows Installer | 1.8.0   | `a9a37ec2677fc7d224c5993f914ba402c9f86c2f909dc5d649f67d08802dc847` |
| Monkey Island v1.8.0_3522_windows.exe                | Windows Installer | 1.8.0   | `4aaa5a99a108ab3cb14b9268a32ac68cb2de4a001ae0e4374ca779824981ea64` |
| Monkey Island v1.8.0_3523_windows.exe                | Windows Installer | 1.8.0   | `4f029d2683cf68e63f8b426fa19df9561add0ed169821b4fc83c2721f0939520` |
| Monkey Island v1.8.0_3525_windows.exe                | Windows Installer | 1.8.0   | `4a660cf5eda5beae844e5a62031972304eaa0432c32708f11d94dc0a501be182` |
| Monkey Island v1.8.0_3525_windowszt.exe              | Windows Installer | 1.8.0   | `980ba04ef9f6395e2885851f906ee3ed57d696a2e984aa1e7a59446a57ce0408` |
| infection_monkey_docker_docker_20200419_160310.tgz   | Docker            | 1.8.0   | `999edc833484f51475db5a56e0557b59d09f520453b8077c60f7d9359b504299` |
| infection_monkey_docker_dockerzt_20200419_160542.tgz | Docker            | 1.8.0   | `87ec632837d4add968831ee7fd271871f89e5b29e251d046ebf100bc94bb755e` |
| Monkey Island v1.8.0_3526_windows.exe                | Windows Installer | 1.8.0   | `6b6c05f3575eef9b95c1624f74953e54654211de4ae1ad738b287e661f002989` |
| Monkey Island v1.8.0_3526_windowszt.exe              | Windows Installer | 1.8.0   | `f181e58820817d76274fab3ee2a7824fc0d5b1f637d7f5c7fe111eb7061844f2` |
| Monkey Island v1.8.0_3527_windows.exe                | Windows Installer | 1.8.0   | `94c2e09ca103bc22206715783616af91e58fe773a04c975d6a09d48d9a5759b2` |
| infection_monkey_docker_docker_20200420_151527.tgz   | Docker            | 1.8.0   | `fe4512fd46c3be6c9416287e3a703e8453a46a17b05404ba72035036946f6dbd` |
| infection_monkey_docker_docker_20200420_153306.tgz   | Docker            | 1.8.0   | `17ef5de58a49168a70085cb80063355ac489139c88d029d175a09e36524fe224` |
| infection_monkey_docker_docker_20200420_174533.tgz   | Docker            | 1.8.0   | `fcf57ab8b1b77bcf678765c90798b950fd4a62019c48ebeeac37e9d3011b6b2e` |
| infection_monkey_docker_docker_20200427_184208.tgz   | Docker            | 1.8.0   | `082165abd8c45d9731472ae0877fecedfbcefcff8c0003b43d4300854908f0cb` |
| infection_monkey_docker_dockerzt_20200427_184441.tgz | Docker            | 1.8.0   | `74f824ecb14f5d47182156999d5aeaf2177d719c6f53ed81b68606b2ed931647` |
| Monkey Island v1.8.0_3528_windows.exe                | Windows Installer | 1.8.0   | `baa13321c88223acd0262137ba018f9cbea869b5d1920565a5e6c8eb2c83b80e` |
| Monkey Island v1.8.0_3528_windowszt.exe              | Windows Installer | 1.8.0   | `466f7c3aa052163f10e154ec787b31a98b54ced8cffc17373525e8ca39ec2556` |
| monkey-island-vmware.ova                             | OVA               | 1.8.0   | `6BC4E85A0EA81045BD88E2D5A9F98F0DD40DE99E94D1E343D13FA418045A6915` |
| monkey-island-vmwarezt.ova                           | OVA               | 1.8.0   | `79A043D85521F94024F8B0428A7A33B4D3F5B13F9D2B83F72C73C8D0BB12ED91` |
| monkey_island_vmware.deb                             | VMWare Debian     | 1.7.0   | `8F77347343B1D070C4BCC43A6CF5971F086665206F76AD1304359ADB388C55DE` |
| dk.monkeyisland.latest.tar                           | Docker            | 1.7.0   | `E92CD45DB172342FE906FEFA7F26BACB2F59C2BE8484756B71CD1BDEBCCA8BFB` |
| monkey-windows-32.exe                                | Agent             | 1.7.0   | `00E121EC8AA3519498D225066A3BC29984A7DA2A6F4F0641ED465FD64107A117` |
| Monkey Island v1.7.0.3478.exe                        | Windows Installer | 1.7.0   | `AFC969884939DBE37DA6B8AD4999CA6E9F18E54BA03AC0C04C59ABB6D6204634` |
| monkey_island.deb                                    | Debian            | 1.7.0   | `4AE051BC47B39FA05937994B3D24226771D03891AB2EA484FD7B4AADC0C5E220` |
| monkey-windows-64.exe                                | Agent             | 1.7.0   | `BCF60E0C4BC2578361CCACDA0C183B726AF375F0142306CA9013A14BBA9B962C` |
| monkey-linux-64                                      | Agent             | 1.7.0   | `333529B3061473BF5EE713FA7E3DF4B05DD01823840BB92E1E715488A749B9EA` |
| monkey-linux-32                                      | Agent             | 1.7.0   | `EF7A72FFDDF3A54C74F458201A45B51B779A68C460A309B0D5FD247264D7137D` |
| Monkey Island 1.7.0 OVA 20191013.ova                 | OVA               | 1.7.0   | `EB1D568F1EA9236B3402A65484EE1F06350FF5C4097288F3FE3312474ECB48C7` |
| dk.monkeyisland.latest.zt.tar                        | Docker            | 1.7.0   | `C998FD7CC73F394CD39450E49586397F721D8B7F2DFA4CFE30EC797864588C72` |
| Monkey Island v1.7.0 zt.exe                          | Windows Installer | 1.7.0   | `5C6DADDD3BCF0766DB515DC911DC80D7D11DFF8A72BCBBBE21DEB3C9F78B6889` |
| monkey_island_zt.deb                                 | Debian            | 1.7.0   | `A0515FBCFD9590CEA739E1AFA95CE7FC406C5E4206A67A50C8CD2423540818C8` |
| monkey_island_vmware_zt.deb                          | VMWare Debian     | 1.7.0   | `80EDB3FB846251C7B80B72259837629F17A4166C34FE440451BDD7ED8CC43F7F` |
| Monkey Island 1.7.0 ZT OVA 20191013.ova              | OVA               | 1.7.0   | `D220E171CF38DCD434AB4473C72CE29873A495B16FFAA8CA55658F5606398E34` |
| infection_monkey_deb_vmware.20190519_125330.tgz      | VMWare            | 1.6.3   | `22e51f089e6537e2cb349b07b4bf22c7a63c68ae12776a7b5239a0238bf02a05` |
| infection_monkey_deb_gcp.20190519_125239.tgz         | GCP               | 1.6.3   | `b8fdb976af8130329265bd3ad36b553864f6f7a2a2df912cfea4215584774686` |
| infection_monkey_docker.20190519_125632.tgz          | Docker            | 1.6.3   | `5576e20fe8ee502a7b452b504789961aedae214e49061a58ca0f248cc72c1c78` |
| monkey-windows-32.exe                                | Agent             | 1.6.3   | `6f68d436a2a85852b02e4d72d4202919753a78e5285c36bd1a5481c8711b1d6b` |
| Monkey Island v1.6.3.3468.exe                        | Windows Installer | 1.6.3   | `69cb63612855165db97eb3c253e5a6f627fe216e0610eca5e5e6f875281a3604` |
| infection_monkey_deb.20190519_124555.tgz             | Debian            | 1.6.3   | `2389b553bd569defa4b81053984f0743b1b4093cdcfcf8561243b9d882d55e83` |
| monkey-windows-64.exe                                | Agent             | 1.6.3   | `502c749ede6e09b8c40bc4bbfd2a46c95d3626a1aef74c72ac7b5641595e8c9c` |
| monkey-linux-64                                      | Agent             | 1.6.3   | `6cfec4aea2f993294ca32f816a85347be8b155fb9c39706c82866bce8d8f87c1` |
| monkey-linux-32                                      | Agent             | 1.6.3   | `996b3883e9b1114b274bf25426ee13060b65f8deb08c96b57857b99d8e8e3277` |
| Infection Monkey 1.6.3.ova                           | OVA               | 1.6.3   | `a5b6e7d547ad4ae79508301698d99cbaf3b3ebfb1d2f0274ae1151d803def1e4` |
| infection_monkey_deb_azure.20190519_125317.tgz       | Azure             | 1.6.3   | `fcf1b6bf805f4422deb90f25752573f796d5a73e148086f49db310208b02c829` |
| infection_monkey_deb_aws.20190519_130517.tgz         | AWS               | 1.6.3   | `9c232f5d2f9dc24c9faea3cf597af783798baedb61334e0e650ca79bdac29fec` |
| Infection Monkey 1.6.2.ova                           | OVA               | 1.6.2   | `00346E6383E7BBDB107C14B668D251513E150C089A26AAFA3E17040D96C7DEC9` |
| infection_monkey_deb.1.6.2.tgz                       | Debian            | 1.6.2   | `56BF1D99DD6674F9D3504D5DD5A62D8B3520B4F25449ED0026E5A0DC99BD0683` |
| infection_monkey_1.5_docker.tgz                      | Docker            | 1.6.2   | `2466B4FFFE175EC5DEF0CAACF93EE5CC7D8878DBA63B30F148C560A6AFA5B537` |
| Monkey Island v1.6.2.3434.exe                        | Windows Installer | 1.6.2   | `2B0BFD5721897787536F4F94D5641E061833CBEF0279C0E38C41BC1B3E76A380` |
| Monkey-Linux-32                                      | Agent             | 1.6.1   | `9E5F8FA7F85FEB1BC31E0AE7D1F303139CA3FE5FA044E6C58F68B4917D27CACE` |
| Monkey-Linux-64                                      | Agent             | 1.6.1   | `74F9FFBB504FF5E74EFF1399685C0C110EDE0D3244F61591D77EE7A22672457E` |
| Monkey-Windows-32.exe                                | Agent             | 1.6.1   | `53AC0F047CA95A0476944559F6FC650ADA865891139FA1258B35A5A525BC6002` |
| Monkey-Windows-64.exe                                | Agent             | 1.6.1   | `53019FD25CD4A0AE526696EB05E2EEDE32607263C5F29BE36554D637532D41C3` |
| infection_monkey_1.5.2.ova                           | OVA               | 1.5.2   | `6E6CAABBA7CCDB20E981147560353EC731B1FC8955D0319886D36E9825C201C7` |
| infection_monkey_1.5_deb.tgz                         | Debian            | 1.5.2   | `E84EFA3C20A417D13DC6EA64CB046D40ED7534A6FBB91EBF6EA061716A855A17` |
| infection_monkey_1.5_docker.tgz                      | Docker            | 1.5.2   | `0D33C17556FAC28874A2FE9157DB311892B42669E51C043C4DAE2F68B0D74B8F` |
| Monkey-Linux-32                                      | Agent             | 1.5.2   | `4DF689A845FD7092E81ECB0AB5207621836B3D46B71FB3829E5E5CF9DDAF52D0` |
| Monkey-Linux-64                                      | Agent             | 1.5.2   | `99FC4BB24D2EFF1CD107CCE932EA0BDC006ED2226AE0DC19DD0BC7A97ADB553F` |
| Monkey-Windows-32.exe                                | Agent             | 1.5.2   | `8FC1441B87BDFD786A3A262542C013E4C84AC870C847A919CDA0851F91A511B9` |
| Monkey-Windows-64.exe                                | Agent             | 1.5.2   | `0AE8F0AB190E8BEAE78AB12C8477C924FE92B19B1E079B279F4F87AE4BD2A718` |
| infection_monkey_deb.20180402_184213.tgz             | Debian            | 1.5.1   | `4425FC97DE825715837783258FD8BCF88E87AAB3500F63D287384B9D74D54122` |
| Monkey Island v1.5.1.3377.exe                        | Windows Installer | 1.5.1   | `5A137ADA97F39F4C3CA278E851D2684B929911639E2876EB4DF1D1AC5D70E27D` |
| infection_monkey_docker.20180402_184212.tgz          | Docker            | 1.5.1   | `049831C3F9C959128C5C8D9843819A4ED960FF046B1536216B5FA5FF4B28D1A6` |
| Monkey-Linux-32                                      | Agent             | 1.6     | `665E1263347B9D0245211676496E91669809B3865ED8B5AD1878DA54A9784F5C` |
| Monkey-Linux-64                                      | Agent             | 1.6     | `F0D51E7431CF07A842D4D25AAE2DD8A6B9EE08744914729AF448F92088798F7F` |
| Monkey-Windows-32.exe                                | Agent             | 1.6     | `77AC4264715A6E7D238F8B67ED04EE75CF75C07D360A4B649CA6E31C83CE7B21` |
| Monkey-Windows-64.exe                                | Agent             | 1.6     | `0DEED0AA00F7D54B084EF6888731B0CFEC6382045A74B55162FDD3D00D0BE9F8` |
| Monkey Island v1.6.0.3414.exe                        | Windows installer | 1.6     | `242879983A709D7CD6D7D7EEC493442B7FACC8E215CBB21650915C5EECB8829A` |
| infection_monkey_1.6.ova                             | OVA               | 1.6     | `831FBA09AA49940B1747164BEB6B4AF83BA04FCE35285912AB0B18A7FA1A39D8` |
| infection_monkey_deb.1.6.tgz                         | Debian            | 1.6     | `339EC88DD6A2AB6CB917456AA8970B0F1D36D7335E7D2EE1A34B74047F843542` |
| infection_monkey_docker.1.6.tgz                      | Docker            | 1.6     | `0624CF75C4D208DDC7475636CFE2869BA324DEB88C3860DB2934E7BDA3E664F6` |
| infection_monkey.ova                                 | OVA               | 1.5     | `A6773C4DA8FF7A09C0F3FEE45A25D45830C616AACCEC14C86542462ADCDA1F89` |
| infection_monkey_deb.20180208_175917.tgz             | Debian            | 1.5     | `04E3CD3CD301A44BEE508C1BF993948B89212EF3269D61FB13ECB9FDC25268DB` |
| infection_monkey_docker.20180119_112852.tgz          | Docker            | 1.5     | `4D94C6BB7B4A0177CC1F3E864FB714015619ACB4DD1C4E92D8986BA093F8BD87` |
| Monkey Island v1.5.0.exe                             | Windows installer | 1.5     | `A1D7725AF116AE33CEA9A0E641E61C96E51FAFCCCB598F668EB99E35DE799C7B` |
| infection_monkey_1.5_deb.tgz                         | Debian            | 1.5     | `1433B8A5E778F12C9E8AE4B1BCBF2863E0CC5E001D661C8540804B909B9D83C5` |
| infection_monkey_1.5_docker.tgz                      | Docker            | 1.5     | `22B7FDC4C213F0385AEB9F63E60665470C2862C8C1B45B5B49FBF320570A9082` |
| Monkey Island v1.5.0.3371.exe                        | Windows Installer | 1.5     | `B69997E9920E73F16896D3E793AB721388E5636DB1846D4BFEC1C7A372EE2059` |
| infection_monkey_1.5_deb.tgz                         | Debian            | 1.5     | `00EB499FCC590950723E42784D3502B70EAD8AD396B916AF450AB1A48DF993ED` |
| infection_monkey_1.5_docker.tgz                      | Docker            | 1.5     | `A8670280A07EF6A9F5DC9CEB4B11B25DD7B90C37AD94666A6FFAABD6D105F0CB` |
| Monkey Island v1.5.0.exe                             | Windows Installer | 1.5     | `55F39C8EEB04089F54C10C991A82FE1539BC072E1A7F364D0C720CBF0A28EBB7` |
| Monkey-Linux-32                                      | Agent             | 1.5     | `B85E10AEF0B6935B0AF6EFEA03C9A684859F2DD078B31D9492E98585E2E89C39` |
| Monkey-Linux-64                                      | Agent             | 1.5     | `44BA13A7391D4A16C46D5EF44F60B09E1EDCEB3C716C0AF4241F166619A62944` |
