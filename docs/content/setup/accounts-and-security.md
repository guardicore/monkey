---
title: "Accounts and Security"
date: 2020-06-22T15:36:56+03:00
draft: false
weight: 50
pre: "<i class='fas fa-user-lock'></i> "
tags: ["usage", "password"]
---

## Security in Infection Monkey

The first time you launch Monkey Island (Infection Monkey CC server), you'll be prompted to create an account and secure your island. After your account is created, the server will only be accessible via the credentials you chose.

If you want island to be accessible without credentials press *I want anyone to access the island*. Please note that this option is insecure: you should only pick this for use in development environments.

## Resetting account credentials

To reset credentials edit `monkey_island\cc\server_config.json` by deleting `user` and `password_hash` variables. Then restart the Monkey Island server and you should be prompted with registration form again.

Example `server_config.json` for account reset:

```json
{
  "server_config": "password",
  "deployment": "develop"
}
```
