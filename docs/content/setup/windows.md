---
title: "Windows"
date: 2020-05-26T20:57:10+03:00
draft: false
pre: '<i class="fab fa-windows"></i> '
weight: 2
tags: ["setup", "windows"] 
---

## Deployment

Run the installer, and you should be met with the following screen:

![Windows installer screenshot](../../images/setup/windows/installer-screenshot-1.png "Windows installer screenshot")

1. Follow the steps of the installation.
1. Run the Monkey Island by clicking on the desktop shortcut.

## Troubleshooting

### Missing windows update

The installer requires [Windows update #2999226](https://support.microsoft.com/en-us/help/2999226/update-for-universal-c-runtime-in-windows) to be installed. If you’re having trouble running the installer, please make sure to install that update via Windows Update or manually from the link.

### Supported browsers

The Monkey Island supports Chrome (and Chrome-based) browsers. Some Windows Servers only have Internet Explorer installed. Make sure to use Chrome or a similar modern browser. [You can download Google Chrome from here](https://www.google.com/chrome/).

## Upgrading

To upgrade, download the new installer and run it. The new Monkey version should be installed over the old one.

If you'd like to keep your existing configuration, you can export it to a file by using the Export button and then import it to the new server.

![Export configuration](../../images/setup/export-configuration.png "Export configuration")
