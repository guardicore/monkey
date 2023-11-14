---
title: "Linux"
date: 2020-05-26T20:57:28+03:00
draft: false
pre: '<i class="fab fa-linux"></i> '
weight: 4
tags: ["setup", "AppImage", "linux"]
---

## Supported operating systems

An [AppImage](https://appimage.org/) is a distribution-agnostic, self-running
package that contains an application and everything that it may need to run.

The Infection Monkey AppImage package should run on most modern Linux distros that have FUSE
installed, but the ones that we've tested are:
- BlackArch 2023.04.01
- Kali 2023.1
- Parrot 5.2
- CentOS/Rocky/RHEL 8+
- Debian 11
- openSUSE Leap 15.4
- Ubuntu Bionic 18.04, Focal 20.04, Jammy 22.04

On Windows, AppImage can be run in WSL 2.


## Deployment

1. Make the AppImage package executable:
    ```bash
    chmod u+x InfectionMonkey-v2.3.0.AppImage
    ```
1. Start Monkey Island by running the Infection Monkey AppImage package:
    ```bash
    ./InfectionMonkey-v2.3.0.AppImage
    ```

   If you get errors related to FUSE, you may need to install FUSE 2.X first:
   ```bash
   sudo apt update
   sudo apt install libfuse2
   ```
   More information about fixing FUSE-related errors can be found [here](https://docs.appimage.org/user-guide/troubleshooting/fuse.html).
1. Access the Monkey Island web UI by pointing your browser at
   `https://localhost`. Once you have access to the Monkey Island server, check out the
[getting started page]({{< ref "/usage/getting-started" >}}).

{{% notice info %}}
If you're prompted to delete your data directory and you're not sure what to
do, see the [FAQ]({{< ref
"/faq/#i-updated-to-a-new-version-of-the-infection-monkey-and-im-being-asked-to-delete-my-existing-data-directory-why"
>}}) for more information.
{{% /notice %}}

## Running the Infection Monkey as a service on boot

The Infection Monkey can be installed as a service and run on boot by running the AppImage package
with the following parameters. This requires root permissions, so run `sudo -v` and enter your
password before running the script, if required.
```bash
./InfectionMonkey-v2.3.0.AppImage service --install --user <USERNAME>
```

To uninstall it, run:
```bash
./InfectionMonkey-v2.3.0.AppImage service --uninstall
```

{{% notice info %}}
Service installation has been tested on Ubuntu. This feature may not work
properly on other Linux distributions.
{{% /notice %}}

## Configuring the server

You can configure the server by creating
a [server configuration file](../../reference/server_configuration) and
providing a path to it via command line parameters:

`./InfectionMonkey-v2.3.0.AppImage --server-config="/path/to/server_config.json"`

### Change listening port

The Island API is running on port 5000 and it can't be changed. However, the node server serving
the UI and proxying the requests to the API can be configured to listen on a different port.

1. Stop the Monkey Island process.
1. Modify the `server_config.json` by adding the following lines:
    ```json
    {
      ...
      "node_port": 8080,
      ...
    }
    ```
1. Run the AppImage/service again, Monkey Island server will be accessible on `https://localhost:8080`.

### Start Monkey Island with user-provided certificate

By default, Infection Monkey comes with a [self-signed SSL
certificate](https://aboutssl.org/what-is-self-sign-certificate/). In
enterprise or other security-sensitive environments, it is recommended that the
user provide Infection Monkey with a certificate that has been signed by a
private certificate authority.

1. Terminate the Island process if it's already running.

1. (Optional but recommended) Move your `.crt` and `.key` files to
   `$HOME/.monkey_island`.

1. Make sure that your `.crt` and `.key` files are readable only by you.

    ```bash
    chmod 600 <PATH_TO_KEY_FILE>
    chmod 600 <PATH_TO_CRT_FILE>
    ```

1. Create a [server configuration file and provide the path to the certificate](../../reference/server_configuration).
The server configuration file should look something like:

    ```json
    {
        "ssl_certificate": {
            "ssl_certificate_file": "$HOME/.monkey_island/my_cert.crt",
            "ssl_certificate_key_file": "$HOME/.monkey_island/my_key.key"
        }
    }
    ```

1. Start Monkey Island by running the Infection Monkey AppImage package:
    ```bash
    ./InfectionMonkey-v2.3.0.AppImage --server-config="/path/to/server_config.json"
    ```

1. Access the Monkey Island web UI by pointing your browser at
   `https://localhost`.

### Change logging level

1. Terminate the Island process if it's already running.

1. Create a [server configuration file](../../reference/server_configuration).
The server configuration file should look something like:

    ```json
    {
        "log_level": "INFO"
    }
    ```

1. Start Monkey Island by running the Infection Monkey AppImage package:
    ```bash
    ./InfectionMonkey-v2.3.0.AppImage --server-config="/path/to/server_config.json"
    ```

1. Access the Monkey Island web UI by pointing your browser at
   `https://localhost`.

## Upgrading

Currently, there's no "upgrade-in-place" option when a new version is released.
To get an updated version, download the updated AppImage package and follow the deployment
instructions again.

If you'd like to keep your existing configuration, you can export it to a file
using the *Export config* button and then import it to the new Monkey Island.

![Import/export configuration](../../images/island/configuration_page/import_export_configuration.png "Import/export configuration")
