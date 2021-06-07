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
    tar -xvzf monkey-island-docker.tar.gz
    ```

1. Load the Monkey Island Docker image:

    ```bash
    sudo docker load -i dk.monkeyisland.1.10.0.tar
    ```

### 2. Start MongoDB

1. Start a MongoDB Docker container:

    ```bash
    sudo docker run \
        --name monkey-mongo \
        --network=host \
        --volume db:/data/db \
        --detach mongo:4.2
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
        guardicore/monkey-island:1.10.0
    ```

### 3b. Start Monkey Island with User-Provided Certificate

1. Create a directory named `monkey_island_data`. This will serve as the
   location where Infection Monkey stores its configuration and runtime
   artifacts.

    ```bash
    mkdir ./monkey_island_data
    ```

1. Run Monkey Island with the `--setup-only` flag to populate the `./monkey_island_data` directory with a default `server_config.json` file.

    ```bash
    sudo docker run \
        --rm \
        --name monkey-island \
        --network=host \
        --user $(id -u ${USER}):$(id -g ${USER}) \
        --volume "$(realpath ./monkey_island_data)":/monkey_island_data \
        guardicore/monkey-island:1.10.0 --setup-only
    ```

1. (Optional but recommended) Copy your `.crt` and `.key` files to `./monkey_island_data`.

1. Make sure that your `.crt` and `.key` files are read-only and readable only by you.

    ```bash
    chmod 400 ./monkey_island_data/{*.key,*.crt}
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
        "ssl_certificate_file": "<PATH_TO_CRT_FILE>",
        "ssl_certificate_key_file": "<PATH_TO_KEY_FILE>",
      }
    }
    ```

1. Start the Monkey Island server:

    ```bash
    sudo docker run \
        --name monkey-island \
        --network=host \
        --user $(id -u ${USER}):$(id -g ${USER}) \
        --volume "$(realpath ./monkey_island_data)":/monkey_island_data \
        guardicore/monkey-island:1.10.0
    ```

### 4. Accessing Monkey Island

After the Monkey Island docker container starts, you can access Monkey Island by pointing your browser at `https://localhost:5000`.

## Upgrading

Currently, there's no "upgrade-in-place" option when a new version is released.
To get an updated version, download it, stop the current container and run the
installation commands again with the new file.

If you'd like to keep your existing configuration, you can export it to a file
using the *Export config* button and then import it to the new Monkey Island.

![Export configuration](../../images/setup/export-configuration.png "Export configuration")

## Troubleshooting

### The Monkey Island container crashes due to a 'UnicodeDecodeError'
`UnicodeDecodeError: 'utf-8' codec can't decode byte 0xee in position 0: invalid continuation byte`

You may encounter this error because of the existence of different MongoDB keys in the `monkey-island` and `monkey-mongo` containers.

Starting a new container from the `guardicore/monkey-island:1.10.0` image generates a new secret key for storing sensitive information in MongoDB. If you have an old database instance running (from a previous run of Monkey), the key in the `monkey-mongo` container is different than the newly generated key in the `monkey-island` container. Since encrypted data (obtained from the previous run) is stored in MongoDB with the old key, decryption fails and you get this error.

You can fix this in two ways:
1. Instead of starting a new container for the Monkey Island, you can run `docker container start -a monkey-island` to restart the existing container, which will contain the correct key material.
2. Kill and remove the existing MongoDB container, and start a new one. This will remove the old database entirely. Then, start the new Monkey Island container.
