---
title: "Docker"
date: 2020-05-26T20:57:28+03:00
draft: false
pre: '<i class="fab fa-docker"></i> '
weight: 4
tags: ["setup", "docker", "linux", "windows"]
---

## Deployment

To extract the `tar.gz` file, run `tar -xvzf monkey-island-docker.tar.gz`.

Once you've extracted the container from the tar.gz file, run the following commands:

```sh
sudo docker load -i dk.monkeyisland.1.9.0.tar
sudo docker pull mongo
sudo mkdir -p /var/monkey-mongo/data/db
sudo docker run --name monkey-mongo --network=host -v /var/monkey-mongo/data/db:/data/db -d mongo
sudo docker run --name monkey-island --network=host -d guardicore/monkey-island:1.9.0
```

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
