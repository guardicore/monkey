---
title: "Linux"
date: 2020-05-26T20:57:28+03:00
draft: false
pre: '<i class="fab fa-linux"></i> '
weight: 4
tags: ["setup", "AppImage", "linux"]
---

## Supported operating systems

## Deployment

1. Make the AppImage package executable:
    ```bash
    chmod u+x Infection_Monkey_v1.11.0.AppImage
    ```
1. Start Monkey Island by running the Infection Monkey AppImage package:
    ```bash
    ./Infection_Monkey_v1.11.0.AppImage
    ```
1. Access the Monkey Island web UI by pointing your browser at
   `https://localhost:5000`.

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
    ./Infection_Monkey_v1.11.0.AppImage --setup-only
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
        "ssl_certificate_key_file": "<PATH_TO_KEY_FILE>",
      }
    }
    ```

1. Start Monkey Island by running the Infection Monkey AppImage package:
    ```bash
    ./Infection_Monkey_v1.11.0.AppImage
    ```

1. Access the Monkey Island web UI by pointing your browser at
   `https://localhost:5000`.

## Upgrading
