---
title: "Data directory"
date: 2021-05-18T08:49:59+03:00
draft: false
pre: '<i class="fas fa-folder"></i> '
weight: 9
---

## What is the data directory?

The data directory is where the Island Server stores runtime artifacts. These
include the Island logs, configuration files, etc.

## Where is it located?

On Linux, the default path is `$HOME/.monkey_island`.
On Windows, the default path is `%AppData%\monkey_island`.

## How do I configure the location of the data directory on Linux?

The location of the data directory is set in the `data_dir` field in the
`server_config.json` file.

1. [Create a custom server_config.json file](../server_configuration) and set the `data_dir` field. Its
   contents will look like this:

    ```json
    {
      "log_level": "DEBUG",
      "environment": {
        "server_config": "password"
      },
      "mongodb": {
            "start_mongodb": true
      },
      "data_dir": "<PATH_TO_DATA_DIR>"
    }
    ```

1. Start the Infection Monkey with the `--server-config` parameter.

    ```bash
    $ InfectionMonkey-VERSION.AppImage --server-config <PATH_TO_SERVER_CONFIG>
    ```
