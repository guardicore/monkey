---
title: "Server configuration"
date: 2021-11-26T12:00:19+02:00
draft: true
pre: '<i class="fas fa-cogs"></i> '
weight: 1
---

## Configuring the Island

The Island Server(C&C) is configured by creating a `server_config.json` file.

### Creating a configuration file

Here's an example `server_config.json` with all options specified:
```json
{
  "log_level": "DEBUG",
  "ssl_certificate": {
    "ssl_certificate_file": "<PATH_TO_CRT_FILE>",
    "ssl_certificate_key_file": "<PATH_TO_KEY_FILE>"
  },
  "mongodb": {
    "start_mongodb": true
  },
  "data_dir": "/monkey_island_data"
}
```

Only relevant options can be specified, for example:
```json
{
  "ssl_certificate": {
    "ssl_certificate_file": "<PATH_TO_CRT_FILE>",
    "ssl_certificate_key_file": "<PATH_TO_KEY_FILE>"
  }
}
```

### Applying configuration to the island

#### AppImage (Linux)

Specify the path to the `server_config.json` through a command line argument.

Example: `./InfectionMonkey-v1.12.0.AppImage --server-config="/tmp/server_config.json"`

#### Windows

Move the created `server_config.json` to the install directory, monkey island directory.
If you haven't changed the default install directory, the path should look like:

`C:\Program Files\Guardicore\Monkey Island\monkey\monkey_island\server_config.json`

#### Docker

Best way to configure the docker is to is to map server's [data directory](../data_directory) to a volume:

1. Create a directory for server configuration and other files, e.g. `monkey_island_data`. If you already have it,
   **make sure it's empty**.

    ```bash
    mkdir ./monkey_island_data
    chmod 700 ./monkey_island_data
    ```
1. Establish and populate the created directory with server files (modify the `VERSION` to the one you downloaded):
```bash
sudo docker run \
    --rm \
    --name monkey-island \
    --network=host \
    --user "$(id -u ${USER}):$(id -g ${USER})" \
    --volume "$(realpath ./monkey_island_data)":/monkey_island_data \
    guardicore/monkey-island:VERSION --setup-only
```

Once the volume is mapped, we can put `server_config.json` there.
`server_config.json` for docker **must** contain a valid data directory field and `start_mongodb` set to false.

So, at minimum your `server_config.json` should look like this:

```json
{
  "data_dir": "/monkey_island_data",
  "mongodb": {
    "start_mongodb": false
 }
}
```

Then, the container can be launched by providing `server_config.json` path in the arguments:
```bash
sudo docker run \
    --rm \
    --name monkey-island \
    --network=host \
    --user "$(id -u ${USER}):$(id -g ${USER})" \
    --volume "$(realpath ./monkey_island_data)":/monkey_island_data \
    guardicore/monkey-island:VERSION --server-config="/monkey_island_data/server_config.json"
```
