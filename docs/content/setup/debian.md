---
title: "Debian"
date: 2020-05-26T20:57:19+03:00
draft: false
pre: '<i class="fab fa-linux"></i> '
weight: 1
disableToc: false
tags: ["setup", "debian", "linux"]
---


## Supported Distros

This Debian package has been tested on Ubuntu Bionic 18.04 LTS and Ubuntu Focal 20.04 LTS.

## Deployment

1. Update your package list by running:
    ```sh
    sudo apt update
    ```
1. If you are using Ubuntu Focal 20.04, run the following commands to install
   Python 3.7:
    ```sh
    sudo apt install software-properties-common
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt install python3.7 python3.7-dev
    ```
1. Extract the tarball by running:
    ```sh
    tar -xvzf infection_monkey_deb.tgz
    ```
1. Install the Monkey Island Debian package:
    ```sh
    sudo dpkg -i monkey_island_deb.deb  # this might print errors
    ```
1. If, at this point, you receive dpkg errors that look like this:

    ```sh
    dpkg: error processing package gc-monkey-island (--install):
        dependency problems - leaving unconfigured
    Errors were encountered while processing:
        gc-monkey-island
    ```

    It just means that not all dependencies were pre-installed on your system.
    That's no problem! Just run the following command, which will install all
    dependencies, and then install the Monkey Island:

    ```sh
    sudo apt install -f
    ```

## Troubleshooting

### Trying to install on Ubuntu <16.04

If you're trying to install the Monkey Island on Ubuntu 16.04 or older, you
need to install the dependencies yourself, since Python 3.7 is only installable
from the `deadsnakes` PPA. To install the Monkey Island on Ubuntu 16.04, follow
these steps:

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

Currently, there's no "upgrade-in-place" option when a new version is released.
To get the updated version, download the new `.deb` file and install it. You
should see a message like `Unpacking monkey-island (1.8.2) over (1.8.0)`. After
which, the installation should complete successfully.

If you'd like to keep your existing configuration, you can export it to a file
using the *Export config* button and then import it to the new Monkey Island.

![Export configuration](../../images/setup/export-configuration.png "Export configuration")
