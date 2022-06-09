---
title: "Running Manually"
date: 2022-06-09T14:47:40+03:00
draft: false
weight: 2
pre: "<i class='fas fa-terminal'></i> "
tags: ["usage"]
---


## Generating manual run command

Manual run command can be generated through the Island Server UI, by going to "Run Monkey" -> "Manual" page.

### Downloading the agent manually

As evident by the generated commands, agent binaries can be downloaded
by sending a get request to `https://[IP]:5000/api/agent/download/[OS]`, where
`[IP]` stands for the IP address of the Island server and `[OS]` is either `windows` or `linux`.

### Running the agent binary

Agent binary can be started with `m0nk3y` or `dr0pp3r` flags.

`m0nk3y` flag is the standard way
to run the agent.

`dr0pp3r` will move the agent binary to a location provided with an `-l` flag.
Then it will start that binary with a `m0nk3y` flag on a new process. Finally, it will stop
the current process and shut down. This flag is useful if you want to start the agent on a separate
process. This flag is used by the agent to execute other agents on exploited machines.
This way, the parent agent doesn't have to wait until the child finishes to continue the execution.
