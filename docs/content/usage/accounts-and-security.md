---
title: "Accounts and Security"
date: 2020-06-22T15:36:56+03:00
draft: true
---

## Security in InfectionMonkey

The first time you launch Monkey Island (InfectionMonkey CC server), you'll be prompted to 
create an account and secure your island. After your account is created, the server will only
be accessible via the credentials you chose. 

If you want island to be accessible without credentials press "I want anyone to access the island".
This is an insecure option though and should only be used in development.

## Resetting account credentials

To reset credentials edit `monkey_island\cc\server_config.json` 
by deleting `user` and `password_hash` variables. Then restart Island server and you should be 
prompted with registration form.

Example `server_config.json` for account reset:
```
{
  "server_config": "password",
  "deployment": "develop"
}
```
