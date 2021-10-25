---
title: "Docker"
date: 2020-05-26T20:57:28+03:00
draft: false
pre: '<i class="fab fa-docker"></i> '
weight: 4
tags: ["setup", "docker", "linux", "windows"]
---

## Supported operating systems

The Infection Monkey Docker container works on Linux only. It is not compatible with Docker for Windows or Docker for Mac.

## Deployment

### 1. Load the docker images
1. Pull the MongoDB v4.2 Docker image:

    ```bash
    sudo docker pull mongo:4.2
    ```

1. Extract the Monkey Island Docker tarball:

    ```bash
    tar -xvzf InfectionMonkey-docker-v1.12.0.tgz
    ```

1. Load the Monkey Island Docker image:

    ```bash
    sudo docker load -i InfectionMonkey-docker-v1.12.0.tar
    ```

### 2. Start MongoDB

1. Start a MongoDB Docker container:

    ```bash
    sudo docker run \
        --name monkey-mongo \
        --network=host \
        --volume db:/data/db \
        --detach \
        mongo:4.2
    ```

### 3a. Start Monkey Island with default certificate

By default, Infection Monkey comes with a [self-signed SSL certificate](https://aboutssl.org/what-is-self-sign-certificate/). In
enterprise or other security-sensitive environments, it is recommended that the
user [provide Infection Monkey with a
certificate](#3b-start-monkey-island-with-user-provided-certificate) that has
been signed by a private certificate authority.

1. Run the Monkey Island server
    ```bash
    sudo docker run \
        --name monkey-island \
        --network=host \
        guardicore/monkey-island:VERSION
    ```

### 3b. Start Monkey Island with user-provided certificate

1. Create a directory named `monkey_island_data`. If you already have it,
   **make sure it's empty**. This will serve as the location where Infection
   Monkey stores its configuration and runtime artifacts.

    ```bash
    mkdir ./monkey_island_data
    chmod 700 ./monkey_island_data
    ```

1. Run Monkey Island with the `--setup-only` flag to populate the `./monkey_island_data` directory with a default `server_config.json` file.

    ```bash
    sudo docker run \
        --rm \
        --name monkey-island \
        --network=host \
        --user "$(id -u ${USER}):$(id -g ${USER})" \
        --volume "$(realpath ./monkey_island_data)":/monkey_island_data \
        guardicore/monkey-island:VERSION --setup-only
    ```

1. Move your `.crt` and `.key` files to `./monkey_island_data`.

1. Make sure that your `.crt` and `.key` files are readable and writeable only by you.

    ```bash
    chmod 600 ./monkey_island_data/<KEY_FILE>
    chmod 600 ./monkey_island_data/<CRT_FILE>
    ```

1.  Edit `./monkey_island_data/server_config.json` to configure Monkey Island
    to use your certificate. Your config should look something like this:

    ```json {linenos=inline,hl_lines=["11-14"]}
    {
      "data_dir": "/monkey_island_data",
      "log_level": "DEBUG",
      "environment": {
        "server_config": "password",
        "deployment": "docker"
      },
      "mongodb": {
        "start_mongodb": false
     },
      "ssl_certificate": {
        "ssl_certificate_file": "/monkey_island_data/<CRT_FILE>",
        "ssl_certificate_key_file": "/monkey_island_data/<KEY_FILE>"
      }
    }
    ```

1. Start the Monkey Island server:

    ```bash
    sudo docker run \
        --name monkey-island \
        --network=host \
        --user "$(id -u ${USER}):$(id -g ${USER})" \
        --volume "$(realpath ./monkey_island_data)":/monkey_island_data \
        guardicore/monkey-island:VERSION
    ```

### 4. Accessing Monkey Island

After the Monkey Island docker container starts, you can access Monkey Island by pointing your browser at `https://localhost:5000`.

## Upgrading

Currently, there's no "upgrade-in-place" option when a new version is released.
To get an updated version, download it, stop the current container and run the
installation commands again with the new file.

When running an updated version using a volume make sure that you have empty
volume for the Island. Also make sure that you don't have an old mongodb
volume.

If you'd like to keep your existing configuration, you can export it to a file
using the *Export config* button and then import it to the new Monkey Island.

![Export configuration](../../images/setup/export-configuration.png "Export configuration")

## Troubleshooting

### The Monkey Island container crashes due to a 'UnicodeDecodeError'

You will encounter a `UnicodeDecodeError` if the `monkey-island` container is
using a different secret key to encrypt sensitive data than was initially used
to store data in the `monkey-mongo` container.

```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xee in position 0: invalid continuation byte
```

Starting a new container from the `guardicore/monkey-island:VERSION` image
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
