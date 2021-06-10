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

### Start Monkey Island with user-provided certificcate

By default, Infection Monkey comes with a [self-signed SSL certificate](https://aboutssl.org/what-is-self-sign-certificate/). In
enterprise or other security-sensitive environments, it is recommended that the
user provide Infection Monkey with a certificate that has been signed by a
private certificate authority.

1. If you haven't already, run the Monkey Island by clicking on the desktop
   shortcut. This will populate MongoDB, as well as create and populate
   `%AppData%\monkey_island`.
1. Stop the Monkey Island process.
1. (Optional but recommended) Move your `.crt` and `.key` files to `%AppData%\monkey_island`.
1. Edit `%AppData%\monkey_island\server_config.json` to configure Monkey Island
   to use your certificate. Your config should look something like this:

    ```json {linenos=inline,hl_lines=["11-14"]}
    {
      "log_level": "DEBUG",
      "environment": {
        "server_config": "password",
        "deployment": "windows"
      },
      "mongodb": {
        "start_mongodb": true
     },
      "ssl_certificate": {
        "ssl_certificate_file": "<PATH_TO_CRT_FILE>",
        "ssl_certificate_key_file": "<PATH_TO_KEY_FILE>"
      }
    }
    ```
1. Run the Monkey Island by clicking on the desktop shortcut.

## Troubleshooting

### Missing Windows update

The installer requires [Windows update #2999226](https://support.microsoft.com/en-us/help/2999226/update-for-universal-c-runtime-in-windows).
If you're having trouble running the installer, please make sure to install the
update via Windows Update or manually from the link above.

### Supported browsers

The Monkey Island supports Chrome (and Chrome-based) browsers. If your Windows
server only has Internet Explorer installed, please install Chrome or a similar
modern browser. [You can download Google Chrome
here](https://www.google.com/chrome/).

## Upgrading

To upgrade the Infection Monkey on Windows, download the new installer and run
it. The new Monkey version will be installed over the old version.

If you'd like to keep your existing configuration, you can export it to a file
using the *Export config* button and then import it to the new Monkey Island.

![Export configuration](../../images/setup/export-configuration.png "Export configuration")
