---
title: "Polymorphism"
date: 2023-05-16T15:19:06+05:30
draft: false
weight: 5
pre: "<i class='fas fa-file-signature'></i> "
tags: ["usage", "polymorphism"]
---


## Description
Polymorphic malware, or metamorphic malware, is a kind of malware that repeatedly
modifies its appearance or signature. As a result, no two copies of the malware share
the same hash. This helps the malware evade detection.

Infection Monkey is not truly metamorphic, but it has the ability to emulate this
property by adding random bytes to each Agent before propagation.

## Using Polymorphism

![Polymorphism Configuration](/images/island/configuration_page/polymorphism_configuration.png "Polymorphism configuration")
