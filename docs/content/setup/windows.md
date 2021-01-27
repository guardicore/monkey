---
title: "Windows"
date: 2020-05-26T20:57:10+03:00
draft: false
pre: '<i class="fab fa-windows"></i> '
weight: 2
tags: ["setup", "windows"] 
---

## Deployment

After running the installer, the following prompt should appear on the screen:

![Windows installer screenshot](../../images/setup/windows/installer-screenshot-1.png "Windows installer screenshot")

1. Follow the steps to complete the installation.
1. Run the Monkey Island by clicking on the desktop shortcut.

## Troubleshooting

### Missing Windows update

The installer requires [Windows update #2999226](https://support.microsoft.com/en-us/help/2999226/update-for-universal-c-runtime-in-windows). If you’re having trouble running the installer, please make sure to install the update via Windows Update or manually from the link above.

### Supported browsers

The Monkey Island supports Chrome (and Chrome-based) browsers. If your Windows server only has Internet Explorer installed, please install Chrome or a similar modern browser. [You can download Google Chrome here](https://www.google.com/chrome/).

## Upgrading

To upgrade the Infection Monkey on Windows, download the new installer and run it. The new Monkey version will be installed over the old version.

If you'd like to keep your existing configuration, you can export it to a file using the *Export config* button and then import it to the new server.

![Export configuration](../../images/setup/export-configuration.png "Export configuration")
