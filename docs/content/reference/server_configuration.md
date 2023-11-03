---
title: "Server configuration"
date: 2021-11-26T12:00:19+02:00
draft: true
pre: '<i class="fas fa-cogs"></i> '
weight: 1
---

## Configuring the Monkey Island

The Monkey Island Server is configured through the `server_config.json` file.

{{% notice info %}}
Refer to the [setup guides](../../setup/) to learn how to use
the `server_config.json` file for each deployment.
{{% /notice %}}

### Creating a configuration file

Here's an example `server_config.json` with all options specified:
```json
{
  "node_port": 443,
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

### Configuration options

See setup instructions for your operating system to understand how to apply these.

 - `node_port` - port on that serves the Island UI. It also proxies requests to the Island API. Default is `443`.
 - `log_level` - can be set to `"DEBUG"`(verbose), `"INFO"`(less verbose) or `"ERROR"`(silent, except errors).
 - `ssl_certificate` - contains paths for files, required to run the Island Server with custom certificate.
 - `data_dir` - path to a writeable directory where the Island will store the database and other files.
 - `mongodb` - options for MongoDB. Should not be changed unless you want to run your own instance of MongoDB.
