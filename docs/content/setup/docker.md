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

Once you’ve extracted the container from the tar.gz file, run the following commands:

```sh
sudo docker load -i dk.monkeyisland.1.9.0.tar
sudo docker pull mongo
sudo mkdir -p /var/monkey-mongo/data/db
sudo docker run --name monkey-mongo --network=host -v /var/monkey-mongo/data/db:/data/db -d mongo
sudo docker run --name monkey-island --network=host -d guardicore/monkey-island:1.9.0
```

## Upgrading

There's no "upgrade-in-place" option for Docker. To get the new version, download it, stop the current container, and run the installation commands again with the new file.

If you'd like to keep your existing configuration, you can export it to a file by using the Export button and then import it to the new server.

![Export configuration](../../images/setup/export-configuration.png "Export configuration")
