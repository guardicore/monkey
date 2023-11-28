---
title: "Importing/Exporting Configuration"
date: 2023-11-28T10:08:52Z
draft: false
description: "Configure Infection Monkey by import/export a configuration file."
---

## Export Configuration

You can export the current configuration with or without a password using
**Export** button. It will save any changes to the configuration to a file
which you can later import. Configuration can be unencrypted or
password-encrypted. If you configure any items which you don't want to be in
plaintext in the configuration file, encrypt the configuration file with a
password.

> **_NOTE:_** Make sure that you don't lose your password. Password-encrypted
> configuration file can't be restored if password is lost.

![Export
Configuration](/images/island/configuration_page/export_configuration.png
"Export Configuration")


## Import Configuration

Using **Import** button on this screen you can feed the Infection Monkey a
configuration file which will be applied directy to all configuration options.
If the configuration file is encrypted it will prompt a dialog to enter the
password.

> **_NOTE:_** Configuration file can be outdated as we release new version.
> Make sure you have up-to-date configuration file before importing.

### Blank password Configuration
![Configuration without
password](/images/island/configuration_page/import_configuration.png
"Configuration without password")

### Password-Encrypted Configuration
![Password-encrypted
Configuration](/images/island/configuration_page/import_configuration_password.png
"Password-encrypted Configuration")
