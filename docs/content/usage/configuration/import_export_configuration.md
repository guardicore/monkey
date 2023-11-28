---
title: "Importing and Exporting Configuration"
date: 2023-11-28T10:08:52Z
draft: false
description: "Configure Infection Monkey by importing/exporting a configuration file."
---

## Export configuration

You can export the current configuration by clicking the **Export** button at
the bottom of the configuration page. This will save the configuration to a
file, which you can later import. The configuration file can contain plaintext
or encrypted data. If your configuration contains any sensitive data, such as
usernames and passwords, you can choose a password during export that will be
used to encrypt the file.

> **_NOTE:_** Make sure that you don't lose your password. The data in
> encrypted configuration files can't be recovered if password is lost.

![Export
Configuration](/images/island/configuration_page/export_configuration.png
"Export Configuration")


## Import configuration

You can import a configuration file by clicking the **Import** button at the
bottom of the configuration page. If the configuration file is encrypted you
will be prompted to enter the password.

> **_NOTE:_** Configuration files that were exported from older versions of
> Infection Monkey cannot necessarily be imported into newer versions.

> **_NOTE:_** If a configuration file enables plugins (e.g. exploiters or
> payloads) that are not installed, the Monkey Island will refuse to import it.
> You can install plugins on the [plugin installation page](/usage/plugins/).

### Importing a plaintext configuration file
![Configuration without
password](/images/island/configuration_page/import_configuration.png
"Configuration without password")

### Importing a password-protected (encrypted) configuration file
![Password-encrypted
Configuration](/images/island/configuration_page/import_configuration_password.png
"Password-encrypted Configuration")
