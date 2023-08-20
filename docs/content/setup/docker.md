---
title: "Docker"
date: 2020-05-26T20:57:28+03:00
draft: false
pre: '<i class="fab fa-docker"></i> '
weight: 4
tags: ["setup", "docker", "linux"]
---

# Supported operating systems

The Infection Monkey Docker container works on Linux only. It is not compatible with Docker for Windows or Docker for Mac.

# Deployment

## Step 1: load the docker images
1. Pull the MongoDB v6.0 Docker image:

    ```bash
    sudo docker pull mongo:6.0
    ```

1. Pull the Monkey Island Docker image:

    ```bash
    sudo docker pull infectionmonkey/monkey_island:latest
    ```

## Step 2: start MongoDB
If you are upgrading the Infection Monkey to a new version, be sure to remove any MongoDB containers or volumes associated with the previous version.

1. Start a MongoDB Docker container:

    ```bash
    sudo docker run \
        --name monkey-mongo \
        --network=host \
        --volume db:/data/db \
        --detach \
        mongo:6.0
    ```

## Step 3: start Monkey Island with default certificate

By default, Infection Monkey comes with a [self-signed SSL certificate](https://aboutssl.org/what-is-self-sign-certificate/). In
enterprise or other security-sensitive environments, it is recommended that the
user [provide Infection Monkey with a
certificate](#start-monkey-island-with-user-provided-certificate) that has
been signed by a private certificate authority.

1. Run the Monkey Island Server
    ```bash
    sudo docker run \
        --tty \
        --interactive \
        --name monkey-island \
        --network=host \
        infectionmonkey/monkey-island:latest
    ```

## Step 4: accessing Monkey Island

After the Monkey Island docker container starts, you can access Monkey Island by pointing your browser at `https://localhost:5000`.

# Configuring the server

You can configure the server by mounting a volume and specifying a
 [server configuration file](../../reference/server_configuration):

1. Create a directory for server configuration file, e.g. `monkey_island_data`:
    ```bash
    mkdir -m=0700 ./monkey_island_data
    ```
1. Run the container with a mounted volume, and the `--setup-only` flag:
    ```bash
    sudo docker run \
        --rm \
        --name monkey-island \
        --network=host \
        --user "$(id -u ${USER}):$(id -g ${USER})" \
        --volume "$(realpath ./monkey_island_data)":/monkey_island_data \
        infectionmonkey/monkey-island:latest --setup-only
    ```
1. Move your `server_config.json` file to `./monkey_island_data` directory.
   Your `server_config.json` file must contain at least the following:
    ```json
        {
            "data_dir": "/monkey_island_data",
            "mongodb": {
                "start_mongodb": false
            }
        }
    ```
1. Run the container with a mounted volume, specify the path to the `server_config.json`:
    ```bash
    sudo docker run \
        --rm \
        --name monkey-island \
        --network=host \
        --user "$(id -u ${USER}):$(id -g ${USER})" \
        --volume "$(realpath ./monkey_island_data)":/monkey_island_data \
        infectionmonkey/monkey-island:latest --server-config="/monkey_island_data/server_config.json"
    ```

### Start Monkey Island with user-provided certificate

By default, Infection Monkey comes with a [self-signed SSL
certificate](https://aboutssl.org/what-is-self-sign-certificate/). In
enterprise or other security-sensitive environments, it is recommended that the
user provide Infection Monkey with a certificate that has been signed by a
private certificate authority.

1. If you haven't already, follow the steps above in the [Configuring the
   server](#configuring-the-server) section.
1. Terminate the docker container if it's already running.
1. Move your `.crt` and `.key` files to `./monkey_island_data`.
1. Make sure that your `.crt` and `.key` files are readable only by you.
    ```bash
    chmod 600 <PATH_TO_KEY_FILE>
    chmod 600 <PATH_TO_CRT_FILE>
    ```
1. Modify the [server configuration file](../../reference/server_configuration) to look like:
    ```json
    {
        "data_dir": "/monkey_island_data",
        "mongodb": {
            "start_mongodb": false
        },
        "ssl_certificate": {
            "ssl_certificate_file": "/monkey_island_data/my_cert.crt",
            "ssl_certificate_key_file": "/monkey_island_data/my_key.key"
        }
    }
    ```
1. Run the container with a mounted volume, specify the path to the `server_config.json`:
    ```bash
    sudo docker run \
        --rm \
        --name monkey-island \
        --network=host \
        --user "$(id -u ${USER}):$(id -g ${USER})" \
        --volume "$(realpath ./monkey_island_data)":/monkey_island_data \
        infectionmonkey/monkey-island:latest --server-config="/monkey_island_data/server_config.json"
    ```
1. Access the Monkey Island web UI by pointing your browser at
   `https://localhost:5000`.

### Change logging level

1. Stop the docker container if it's already running.
1. Modify the [server configuration file](../../reference/server_configuration) by adding the following lines:
    ```json
    {
        "log_level": "INFO"
    }
    ```
1. Run the container with a mounted volume, specify the path to the `server_config.json`:
    ```bash
    sudo docker run \
        --rm \
        --name monkey-island \
        --network=host \
        --user "$(id -u ${USER}):$(id -g ${USER})" \
        --volume "$(realpath ./monkey_island_data)":/monkey_island_data \
        infectionmonkey/monkey-island:latest --setup-only --server-config="/monkey_island_data/server_config.json"
    ```
1. Access the Monkey Island web UI by pointing your browser at
   `https://localhost:5000`.

## Upgrading

Currently, there's no "upgrade-in-place" option when a new version is released.
To get an updated version, download it, stop and remove the current Monkey
Island and MongoDB containers and volumes, and run the installation commands
again with the new file.

If you'd like to keep your existing configuration, you can export it to a file
using the *Export config* button and then import it to the new Monkey Island.

![Import/export configuration](https://raw.githubusercontent.com/guardicore/monkey/develop/docs/static/images/island/configuration_page/import_export_configuration.png)

# Troubleshooting

## The Monkey Island container crashes due to a 'UnicodeDecodeError'

You will encounter a `UnicodeDecodeError` if the `monkey-island` container is
using a different secret key to encrypt sensitive data than was initially used
to store data in the `monkey-mongo` container.

```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xee in position 0: invalid continuation byte
```

Starting a new container from the `infectionmonkey/monkey-island:VERSION` image
generates a new secret key for storing sensitive information in MongoDB. If you
have an old database instance running (from a previous instance of Infection
Monkey), the data stored in the `monkey-mongo` container has been encrypted
with a key that is different from the one that Monkey Island is currently
using. When MongoDB attempts to decrypt its data with the new key, decryption
fails and you get this error.

You can fix this in one of three ways:
1. Instead of starting a new container for the Monkey Island, you can run `docker container start -a monkey-island` to restart the existing container, which will contain the correct key material.
1. Kill and remove the existing MongoDB container, and start a new one. This will remove the old database entirely. Then, start the new Monkey Island container.
1. When you start the Monkey Island container, use `--volume
   monkey_island_data:/monkey_island_data`. This will store all of Monkey
   Island's runtime artifacts (including the encryption key file) in a docker
   volume that can be reused by subsequent Monkey Island containers.
