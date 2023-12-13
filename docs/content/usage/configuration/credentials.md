---
title: "Credentials"
date: 2020-06-09T12:20:08+03:00
draft: false
description: "Configure credentials that the Infection Monkey will use for propagation."
---

On this screen, you can configure credentials for Infection Monkey to use when attempting
brute-force attacks. These can be anything from default or weak passwords, to "stolen"
credentials from your network, simulating an attacker with inside knowledge.

![Configure credentials](/images/island/configuration_page/credentials_configuration.png "Configure credentials")

The "Identity" field accepts usernames and email addresses. As seen in the screenshot, the
supported secret types are passwords, LM hashes, NTLM hashes, and SSH keys.

When attempting a brute-force attack, credential combinations that belong to the same row are
tried first. If authentication attempts with those credentials were unsuccessful, all other
possible combinations from the data in the table are tried.

For example, if the input rows are (screenshot below):
1. NT hash `110D0C51E144D36FB7E4F9E012FBB888`
1. Identity `user-1`, password `hello123`
1. Identity `user-2`
1. Identity `user-3`, LM hash `0BEEA40070BB64AA1AA818381E4E281B`

The combinations will be tried in the following order:
1. `user-1:hello123`
1. `user-3:0BEEA40070BB64AA1AA818381E4E281B`
1. `user-1:110D0C51E144D36FB7E4F9E012FBB888` (generated credential combination)
1. `user-1:0BEEA40070BB64AA1AA818381E4E281B` (generated credential combination)
1. `user-2:110D0C51E144D36FB7E4F9E012FBB888` (generated credential combination)
1. `user-2:hello123` (generated credential combination)
1. `user-2:0BEEA40070BB64AA1AA818381E4E281B` (generated credential combination)
1. `user-3:110D0C51E144D36FB7E4F9E012FBB888` (generated credential combination)
1. `user-3:hello123` (generated credential combination)

![Order of configure credentials](/images/island/configuration_page/credentials_configuration_order.png "Order of configured credentials")
