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
- BlackArch 2020.12.01
- Kali 2021.2
- Parrot 4.11
- Rocky 8
- openSUSE Leap 15.3
- Ubuntu Bionic 18.04
- Ubuntu Focal 20.04
- Ubuntu Hirsute 21.04

On Windows, AppImage can be run in WSL 2.


## Deployment

1. Make the AppImage package executable:
    ```bash
    chmod u+x InfectionMonkey-v1.13.0.AppImage
    ```
1. Start Monkey Island by running the Infection Monkey AppImage package:
    ```bash
    ./InfectionMonkey-v1.13.0.AppImage
    ```
1. Access the Monkey Island web UI by pointing your browser at
   `https://localhost:5000`.

{{% notice info %}}
If you're prompted to delete your data directory and you're not sure what to
do, see the [FAQ]({{< ref
"/faq/#i-updated-to-a-new-version-of-the-infection-monkey-and-im-being-asked-to-delete-my-existing-data-directory-why"
>}}) for more information.
{{% /notice %}}

### Start Monkey Island with user-provided certificate

By default, Infection Monkey comes with a [self-signed SSL
certificate](https://aboutssl.org/what-is-self-sign-certificate/). In
enterprise or other security-sensitive environments, it is recommended that the
user provide Infection Monkey with a certificate that has been signed by a
private certificate authority.

1. Run the Infection Monkey AppImage package with the `--setup-only` flag to
   populate the `$HOME/.monkey_island` directory with a default
   `server_config.json` file.

    ```bash
    ./InfectionMonkey-v1.13.0.AppImage --setup-only
    ```

1. (Optional but recommended) Move your `.crt` and `.key` files to
   `$HOME/.monkey_island`.

1. Make sure that your `.crt` and `.key` files are readable only by you.

    ```bash
    chmod 600 <PATH_TO_KEY_FILE>
    chmod 600 <PATH_TO_CRT_FILE>
    ```

1.  Edit `$HOME/.monkey_island/server_config.json` to configure Monkey Island
    to use your certificate. Your config should look something like this:

    ```json {linenos=inline,hl_lines=["11-14"]}
    {
      "data_dir": "~/.monkey_island",
      "log_level": "DEBUG",
      "environment": {
        "server_config": "password",
        "deployment": "linux"
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

1. Start Monkey Island by running the Infection Monkey AppImage package:
    ```bash
    ./InfectionMonkey-v1.13.0.AppImage
    ```

1. Access the Monkey Island web UI by pointing your browser at
   `https://localhost:5000`.

## Upgrading

Currently, there's no "upgrade-in-place" option when a new version is released.
To get an updated version, download the updated AppImage package and follow the deployment
instructions again.

If you'd like to keep your existing configuration, you can export it to a file
using the *Export config* button and then import it to the new Monkey Island.

![Export configuration](../../images/setup/export-configuration.png "Export configuration")
