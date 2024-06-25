---
title: "Polymorphism"
draft: false
pre: "<i class='fas fa-file-signature'></i> "
tags: ["usage", "polymorphism"]
---


## Description

Polymorphic and metamorphic malware are types of malware that modify themselves
during replication. As a result, no two copies of the malware are exactly the
same, which helps the malware evade signature-based detection techniques.

While Infection Monkey is not truly metamorphic, it does have a nifty feature
to emulate an important property of polymorphic and metamorphic malware.
Because each copy of the malware is different, no two copies share the same
hash. By modifying each Agent binary to include some randomized data, the
Infection Monkey Agent can appear polymorphic to some signature-based detection
techniques.


![Polymorphism Configuration](/images/island/configuration-page/polymorphism-configuration.png "Polymorphism configuration")
