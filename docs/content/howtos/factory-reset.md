---
title: "How to perform a factory reset"
draft: false
pre: '<i class="fas fa-eraser"></i> '
tags: ["howtos", "factory reset"]
---

This guide shows you how to perform a factory reset of your Infection Monkey
installation. This is useful if you forgot your credentials for accessing the
Monkey Island or you just want a fresh start.

When the Monkey Island starts for the first time, it creates a [data
directory](/reference/data-directory) where it stores all of its
data if one does not already exist. Performing a factory reset involves the
following steps:

1. Shutdown the Monkey Island (if it's running).
1. Delete the data directory.
1. Restart the Monkey Island.
1. Access the Monkey Island and register a new user.

{{% notice warning %}}
Performing a factory reset will delete all of the data that Infection Monkey
has collected and generated, including the Monkey Island user account, reports,
and configurations.
{{% /notice %}}

### For AppImage (Linux) installations

1. **Stop the Monkey Island.**

    If the Monkey Island is in installed as a systemd service, run:
    ```bash
    $ sudo systemd stop infection-monkey.service
    ```

    Otherwise, navigate to the terminal where you started the Monkey Island and
    enter `<CTRL>+C`.

1. **Locate and delete the data directory.**

    By default, the data directory is located at `$HOME/.monkey_island/`. To
    remove it, run the following command:
    ```bash
    rm -r $HOME/.monkey_island/
    ```

1. **Restart the Monkey Island.**

    If the Monkey Island is installed as a systemd service, run:
    ```bash
    sudo systemd start infection-monkey.service
    ```

    Otherwise, navigate to the directory where the Monkey Island AppImage is and start it with:
    ```bash
    ./InfectionMonkey-<VERSION>.AppImage
    ```

1. **Register a new user.**

    Use your browser to navigate to `https://localhost:5000` (modify the host
    as necessary) and register a new user.


### For Docker installations

1. **Stop the Monkey Island.**
    ```bash
    sudo docker kill monkey-island monkey-mongo
    ```

1. **Delete the MongoDB docker volume.**
    ```bash
    sudo docker volume rm monkey-db
    ```
1. **Delete the Monkey Island container.**
    ```bash
    sudo docker rm monkey-island
    ```
1. **Remove any other volumes that may be associated with Infection Monkey.**

    You can discover other volumes with the command:
    ```bash
    sudo docker volume ls
    ```

    You can remove the volumes with the command:
    ```bash
    sudo docker volume rm <VOLUME_NAME>
    ```

1. **Restart the MongoDB container.**
   ```bash
   sudo docker run \
       --name monkey-mongo \
       --network=host \
       --volume monkey-db:/data/db \
       --detach \
       mongo:6.0
    ```

1. **Restart the Monkey Island container.**
    ```bash
    sudo docker run \
        --name monkey-island \
        --network=host \
        infectionmonkey/monkey-island:latest
    ```

1. **Register a new user.**

    Use your browser to navigate to `https://localhost:5000` (modify the host
    as necessary) and register a new user.

### For Windows installations
1. **Stop the Monkey Island.**

    Locate the command window that the Monkey Island started in. Click the _x_
    in the top right corner of the window to shutdown the Monkey Island.

1. **Locate and delete the data directory.**

    By default, the data directory is located at `%AppData%\monkey_island\`.
    Remove the directory entirely by using the **File Explorer**.

1. **Restart the Monkey Island.**

    Locate the Infection Monkey icon on your desktop and double click it, or
    search "MonkeyIsland" in the **Start** menu and click the Infection Monkey
    icon.

1. **Register a new user.**

    Use your browser to navigate to `https://localhost:5000` (modify the host
    as necessary) and register a new user.
