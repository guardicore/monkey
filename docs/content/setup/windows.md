---
title: "Windows"
date: 2020-05-26T20:57:10+03:00
draft: false
pre: '<i class="fab fa-windows"></i> '
weight: 2
tags: ["setup", "windows"]
---

## Deployment

{{% notice tip %}}
Don't get scared if the Infection Monkey gets [flagged as malware during the installation](/faq/#is-the-infection-monkey-a-malwarevirus).
{{% /notice %}}

After running the installer, the following prompt should appear on the screen:

![Windows installer screenshot](../../images/island/others/windows_installer.png "Windows installer screenshot")

1. Follow the steps to complete the installation.
1. Run the Infection Monkey by clicking on the desktop shortcut. **Note**: If you want Agents to
collect more data on the current machine, consider running as Administrator.

{{% notice info %}}
If you're prompted to delete your data directory and you're not sure what to
do, see the [FAQ]({{< ref
"/faq/#i-updated-to-a-new-version-of-the-infection-monkey-and-im-being-asked-to-delete-my-existing-data-directory-why"
>}}) for more information.
{{% /notice %}}

Once you have access to the Monkey Island server, check out the [getting started page]({{< ref "/usage/getting-started" >}}).

## Configuring the server

You can configure the server by editing [the configuration
file](../../reference/server_configuration) located in installation directory.
The default path is
`C:\Program Files\Infection Monkey\monkey_island\cc\server_config.json`.

### Change listening port

The Island server can be accessed on port 443 by default. On that port javascript runtime (Node server)
serves the UI and proxies requests to the backend API.

It can be changed by modifying the `server_config.json` file:

1. Stop the Monkey Island process.
1. Modify the `server_config.json` by adding the following lines:
    ```json
    {
      ...
      "javascript_runtime_port": 8080,
      ...
    }
    ```
1. Run the Monkey Island again, it will be accessible on `https://localhost:8080`.

The backend API is served on port 5000 and this port can't be changed.

### Start Monkey Island with user-provided certificate

By default, Infection Monkey comes with a [self-signed SSL certificate](https://aboutssl.org/what-is-self-sign-certificate/). In
enterprise or other security-sensitive environments, it is recommended that the
user provide Infection Monkey with a certificate that has been signed by a
private certificate authority.

1. Stop the Monkey Island process.
1. (Optional but recommended) Move your `.crt` and `.key` files to `%AppData%\monkey_island`.
1. Modify the `server_config.json` (by default located in `C:\Program Files\Infection Monkey\monkey_island\cc\server_config.json`) by adding the following lines:
    ```json
    {
      ...
      "ssl_certificate": {
            "ssl_certificate_file": "%AppData%\\monkey_island\\my_cert.crt",
            "ssl_certificate_key_file": "%AppData%\\monkey_island\\my_key.key"
      },
      ...
    }
    ```
1. Run the Monkey Island by clicking on the desktop shortcut.
1. Access the Monkey Island web UI by pointing your browser at
   `https://localhost`.

### Change logging level

1. Stop the Island Server.
1. Modify the `server_config.json` (by default located in `C:\Program Files\Infection Monkey\monkey_island\cc\server_config.json`) by adding the following lines:
    ```json
    {
        ...
        "log_level": "INFO",
        ...
    }
    ```
1. Run the Monkey Island by clicking on the desktop shortcut.
1. Access the Monkey Island web UI by pointing your browser at
   `https://localhost`.

## Troubleshooting

### Support

Only **English** system locale is supported. If your command prompt gives output in a different
language, the Infection Monkey is not guaranteed to work.

For supported Windows versions, take a look at the [OS support page](../../reference/operating_systems_support).

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

![Import/export configuration](../../images/island/configuration_page/import_export_configuration.png "Import/export configuration")
