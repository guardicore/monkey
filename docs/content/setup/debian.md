---
title: "Debian"
date: 2020-05-26T20:57:19+03:00
draft: false
pre: '<i class="fab fa-linux"></i> '
weight: 1
disableToc: false
tags: ["setup", "debian", "linux"]
---

## Deployment

To extract the `tar.gz` file, run `tar -xvzf monkey-island-debian.tar.gz`.

To deploy the package, once you’ve extracted it, run the following commands:

```sh
sudo apt update
sudo dpkg -i monkey_island.deb  # this might print errors
```

If at this point, dpkg printed errors that look like this:

```sh
dpkg: error processing package gc-monkey-island (--install):
    dependency problems - leaving unconfigured
Errors were encountered while processing:
    gc-monkey-island
```

That just means that not all dependencies were pre-installed on your system. That’s no problem! Just run the following command, which will install all dependencies and then install the Monkey Island:

```sh
sudo apt install -f
```

## Troubleshooting

### Trying to install on Ubuntu <16.04

If you’re trying to install the Monkey Island on Ubuntu 16.04 or older, you need to install the dependencies yourself, since Python 3.7 is only installable from the `deadsnakes` PPA. To install the Monkey Island on Ubuntu 16.04, follow the following steps:

```sh
sudo apt update
sudo apt-get install libcurl4-openssl-dev
sudo apt-get install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.7-dev python3.7-venv python3-venv build-essential
sudo dpkg -i monkey_island.deb  # this might print errors
sudo apt install -f
```

### The Monkey Island interface isn't accessible after installation

To check the status of the Monkey Island after the installation, run the following command: `sudo service monkey-island status`.

## Upgrading

To upgrade when a new version comes out, download the new Monkey `.deb` file and install it. You should see a message like `Unpacking monkey-island (1.8.2) over (1.8.0)`. After which, the installation should complete successfully.

If you'd like to keep your existing configuration, you can export it to a file by using the Export button and then import it to the new server.

![Export configuration](../../images/setup/export-configuration.png "Export configuration")
