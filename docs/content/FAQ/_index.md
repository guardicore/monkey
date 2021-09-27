---
title: "FAQ"
date: 2020-06-18T15:11:52+03:00
draft: false
pre: "<i class='fas fa-question'></i> "
---

Below are some of the most common questions we receive about the Infection Monkey. If the answer you're looking for isn't here, talk with us [on our Slack channel](https://infectionmonkey.slack.com/join/shared_invite/enQtNDU5MjAxMjg1MjU1LWM0NjVmNWE2ZTMzYzAxOWJiYmMxMzU0NWU3NmUxYjcyNjk0YWY2MDkwODk4NGMyNDU4NzA4MDljOWNmZWViNDU), email us at [support@infectionmonkey.com](mailto:support@infectionmonkey.com) or [open an issue on GitHub](https://github.com/guardicore/monkey).

- [Where can I get the latest version of the Infection Monkey?](#where-can-i-get-the-latest-version-of-the-infection-monkey)
- [How long does a single Infection Monkey agent run? Is there a time limit?](#how-long-does-a-single-infection-monkey-agent-run-is-there-a-time-limit)
- [Is the Infection Monkey a malware/virus?](#is-the-infection-monkey-a-malwarevirus)
- [Reset/enable the Monkey Island password](#resetenable-the-monkey-island-password)
- [Should I run the Infection Monkey continuously?](#should-i-run-the-infection-monkey-continuously)
  - [Which queries does the Infection Monkey perform to the internet exactly?](#which-queries-does-the-infection-monkey-perform-to-the-internet-exactly)
- [Logging and how to find logs](#logging-and-how-to-find-logs)
  - [Monkey Island server](#monkey-island-server)
  - [Infection Monkey agent](#infection-monkey-agent)
  - [How do I change the log level of the Monkey Island logger?](#how-do-i-change-the-log-level-of-the-monkey-island-logger)
- [Running the Infection Monkey in a production environment](#running-the-infection-monkey-in-a-production-environment)
  - [How much of a footprint does the Infection Monkey leave?](#how-much-of-a-footprint-does-the-infection-monkey-leave)
  - [What's the Infection Monkey's impact on system resources usage?](#whats-the-infection-monkeys-impact-on-system-resources-usage)
  - [Is it safe to use real passwords and usernames in the Infection Monkey's configuration?](#is-it-safe-to-use-real-passwords-and-usernames-in-the-infection-monkeys-configuration)
  - [How do you store sensitive information on Monkey Island?](#how-do-you-store-sensitive-information-on-monkey-island)
  - [How stable are the exploitations used by the Infection Monkey? Will the Infection Monkey crash my systems with its exploits?](#how-stable-are-the-exploitations-used-by-the-infection-monkey-will-the-infection-monkey-crash-my-systems-with-its-exploits)
- [After I've set up Monkey Island, how can I execute the Infection Monkey?](#after-ive-set-up-monkey-island-how-can-i-execute-the-infection-monkey-agent)
- [How can I make the Infection Monkey agents propagate “deeper” into the network?](#how-can-i-make-the-infection-monkey-agent-propagate-deeper-into-the-network)
- [What if the report returns a blank screen?](#what-if-the-report-returns-a-blank-screen)
- [Can I limit how the Infection Monkey propagates through my network?](#can-i-limit-how-the-infection-monkey-propagates-through-my-network)
- [How can I get involved with the project?](#how-can-i-get-involved-with-the-project)

## Where can I get the latest version of the Infection Monkey?

For the latest **stable** release, visit [our downloads page](https://www.guardicore.com/infectionmonkey/#download). **This is the recommended and supported version**!

If you want to see what has changed between versions, refer to the [releases page on GitHub](https://github.com/guardicore/monkey/releases). For the latest development version, visit the [develop version on GitHub](https://github.com/guardicore/monkey/tree/develop).

## How long does a single Infection Monkey agent run? Is there a time limit?

The Infection Monkey agent shuts off either when it can't find new victims or it has exceeded the quota of victims as defined in the configuration.

## Is the Infection Monkey a malware/virus?

The Infection Monkey is not malware, but it uses similar techniques to safely
simulate malware on your network.

Because of this, the Infection Monkey gets flagged as malware by some antivirus
solutions during installation. If this happens, [verify the integrity of the
downloaded installer](/usage/file-checksums) first. Then, create a new folder
and disable antivirus scan for that folder. Lastly, re-install the Infection
Monkey in the newly created folder.

## Reset/enable the Monkey Island password

When you first access the Monkey Island server, you'll be prompted to create an account.
To reset the credentials, edit the `server_config.json` file manually
(located in the [data directory](/reference/data_directory)).

In order to reset the credentials, the following edits need to be made:
1. Delete the `user` field. It will look like this:
```json
{
  ...
  "user": "username",
  ...
}
```
1. Delete the `password_hash` field. It will look like this:
```json
{
  ...
  "password_hash": "$2b$12$d050I/MsR5.F5E15Sm7EkunmmwMkUKaZE0P0tJXG.M9tF.Kmkd342",
  ...
}
```
1. Set `server_config` to `password`. It should look like this:
```json
{
  ...
  "environment": {
    ...
    "server_config": "password",
    ...
  },
  ...
}
```
 Then, reset the Monkey Island process.
 On Linux, use `sudo systemctl restart monkey-island.service`.
 On Windows, restart the program.
 Finally, go to the Monkey Island's URL and create a new account.

## Should I run the Infection Monkey continuously?

Yes! This will allow you to verify that the Infection Monkey identified no new security issues since the last time you ran it.

Does the Infection Monkey require a connection to the internet?

The Infection Monkey does not require internet access to function.

If internet access is available, the Infection Monkey will use the internet for two purposes:

- To check for updates.
- To check if machines can reach the internet.

### Exactly what internet queries does the Infection Monkey perform?

The Monkey performs queries out to the Internet on two separate occasions:

1. The Infection Monkey agent checks if it has internet access by performing requests to pre-configured domains. By default, these domains are `monkey.guardicore.com` and `www.google.com`, which can be changed.  The request doesn't include any extra information - it's a GET request with no extra parameters. Since the Infection Monkey is 100% open-source, you can find the domains in the configuration [here](https://github.com/guardicore/monkey/blob/85c70a3e7125217c45c751d89205e95985b279eb/monkey/infection_monkey/config.py#L152) and the code that performs the internet check [here](https://github.com/guardicore/monkey/blob/85c70a3e7125217c45c751d89205e95985b279eb/monkey/infection_monkey/network/info.py#L123). This **IS NOT** used for statistics collection.
1. After installing the Monkey Island, it sends a request to check for updates on `updates.infectionmonkey.com`. The request doesn't include any PII other than the IP address of the request. It also includes the server's deployment type (e.g., Windows Server, Debian Package, AWS Marketplace) and the server's version (e.g., "1.6.3"), so we can check if we have an update available for this type of deployment. Since the Infection Monkey is 100% open-source, you can inspect the code that performs this [here](https://github.com/guardicore/monkey/blob/85c70a3e7125217c45c751d89205e95985b279eb/monkey/monkey_island/cc/services/version_update.py#L37). This **IS** used for statistics collection. However, due to this data's anonymous nature, we use this to get an aggregate assumption of how many deployments we see over a specific time period - it's not used for "personal" tracking.

## Logging and how to find logs

### Monkey Island server logs

You can download the Monkey Island's log file directly from the UI. Click the "log" section and choose **Download Monkey Island internal logfile**, like so:

![How to download Monkey Island internal log file](/images/faq/download_log_monkey_island.png "How to download Monkey Island internal log file")

It can also be found as a local file on the Monkey Island server system in the specified
[data directory](/reference/data_directory).

The log enables you to see which requests were requested from the server and extra logs from the backend logic. The log will contain entries like these:

```log
2019-07-23 10:52:23,927 - wsgi.py:374 -       _log() - INFO - 200 GET /api/local-monkey (10.15.1.75) 17.54ms
2019-07-23 10:52:23,989 - client_run.py:23 -        get() - INFO - Monkey is not running
2019-07-23 10:52:24,027 - report.py:580 - get_domain_issues() - INFO - Domain issues generated for reporting
```

### Infection Monkey agent logs

The Infection Monkey agent log file can be found in the following paths on machines where it was executed:

- Path on Linux: `/tmp/user-1563`
- Path on Windows: `%temp%\\~df1563.tmp`

The logs contain information about the internals of the Infection Monkey agent's execution. The log will contain entries like these:

```log
2019-07-22 19:16:44,228 [77598:140654230214464:INFO] main.main.116: >>>>>>>>>> Initializing monkey (InfectionMonkey): PID 77598 <<<<<<<<<<
2019-07-22 19:16:44,231 [77598:140654230214464:INFO] monkey.initialize.54: Monkey is initializing...
2019-07-22 19:16:44,231 [77598:140654230214464:DEBUG] system_singleton.try_lock.95: Global singleton mutex '{2384ec59-0df8-4ab9-918c-843740924a28}' acquired
2019-07-22 19:16:44,234 [77598:140654230214464:DEBUG] monkey.initialize.81: Added default server: 10.15.1.96:5000
2019-07-22 19:16:44,234 [77598:140654230214464:INFO] monkey.start.87: Monkey is running...
2019-07-22 19:16:44,234 [77598:140654230214464:DEBUG] control.find_server.65: Trying to wake up with Monkey Island servers list: ['10.15.1.96:5000', '192.0.2.0:5000']
2019-07-22 19:16:44,235 [77598:140654230214464:DEBUG] control.find_server.78: Trying to connect to server: 10.15.1.96:5000
2019-07-22 19:16:44,238 [77598:140654230214464:DEBUG] connectionpool._new_conn.815: Starting new HTTPS connection (1): 10.15.1.96:5000
2019-07-22 19:16:44,249 [77598:140654230214464:DEBUG] connectionpool._make_request.396: https://10.15.1.96:5000 "GET /api?action=is-up HTTP/1.1" 200 15
2019-07-22 19:16:44,253 [77598:140654230214464:DEBUG] connectionpool._new_conn.815: Starting new HTTPS connection (1): updates.infectionmonkey.com:443
2019-07-22 19:16:45,013 [77598:140654230214464:DEBUG] connectionpool._make_request.396: https://updates.infectionmonkey.com:443 "GET / HTTP/1.1" 200 61
```

### How do I change the log level of the Monkey Island logger?

The log level of the Monkey Island logger is set in the `log_level` field
in the `server_config.json` file (located in the [data directory](/reference/data_directory)).
Make sure to leave everything else in `server_config.json` unchanged:

```json
{
  ...
  "log_level": "DEBUG",
  ...
}
```

Logging levels correspond to [the logging level constants in python](https://docs.python.org/3.7/library/logging.html#logging-levels).

To apply the changes, reset the Monkey Island process.
On Linux, use `sudo systemctl restart monkey-island.service`.
On Windows, restart the program.

## Running the Infection Monkey in a production environment

### How much of a footprint does the Infection Monkey leave?

The Infection Monkey leaves hardly any trace on the target system. It will leave:

- Log files in the following locations:
  - Path on Linux: `/tmp/user-1563`
  - Path on Windows: `%temp%\\~df1563.tmp`

### What's the Infection Monkey's impact on system resources usage?

The Infection Monkey uses less than a single-digit percent of CPU time and very low RAM usage. For example, on a single-core Windows Server machine, the Infection Monkey consistently uses 0.06% CPU, less than 80MB of RAM and a small amount of I/O periodically.

If you do experience any performance issues please let us know on [our Slack channel](https://infectionmonkey.slack.com/) or [open an issue on GitHub](https://github.com/guardicore/monkey).

### Is it safe to use real passwords and usernames in the Infection Monkey's configuration?

Absolutely! User credentials are stored encrypted in the Monkey Island server. This information is accessible only to users that have access to the specific Monkey Island.

We advise users to limit access to the Monkey Island server by following our [password protection guide]({{< ref "/setup/accounts-and-security" >}}).

### How do you store sensitive information on Monkey Island?

Sensitive data such as passwords, SSH keys and hashes are stored on the Monkey Island's database in an encrypted fashion. This data is transmitted to the Infection Monkey agents in an encrypted fashion (HTTPS) and is not stored locally on victim machines.

When you reset the Monkey Island configuration, the Monkey Island wipes the information.

### How stable are the exploits used by the Infection Monkey? Will the Infection Monkey crash my systems with its exploits?

The Infection Monkey does not use any exploits or attacks that may impact the victim system.

This means we avoid using some powerful (and famous) exploits such as [EternalBlue](https://www.guardicore.com/2017/05/detecting-mitigating-wannacry-copycat-attacks-using-guardicore-centra-platform/). This exploit was used in WannaCry and NotPetya with huge impact, but, because it may crash a production system, we aren't using it.

## After I've set up Monkey Island, how can I execute the Infection Monkey agent?

See our detailed [getting started]({{< ref "/usage/getting-started" >}}) guide.

## How can I make the Infection Monkey agent propagate “deeper” into the network?

If you wish to simulate a very “deep” attack into your network, you can increase the *propagation depth* parameter in the configuration. This parameter tells the Infection Monkey how far to propagate into your network from the “patient zero” machine.

To do this, change the *Distance from Island* parameter in the “Basic - Network” tab of the configuration:

![How to increase propagation depth](/images/faq/prop_depth.png "How to increase propagation depth")

## What if the report returns a blank screen?

This is sometimes caused when Monkey Island is installed with an old version of MongoDB. Make sure your MongoDB version is up to date using the `mongod --version` command on Linux or the `mongod -version` command on Windows. If your version is older than **4.0.10**, this might be the problem. To update your Mongo version:

- **Linux**: First, uninstall the current version with `sudo apt uninstall mongodb` and then install the latest version using the [official MongoDB manual](https://docs.mongodb.com/manual/administration/install-community/).
- **Windows**: First, remove the MongoDB binaries from the `monkey\monkey_island\bin\mongodb` folder. Download and install the latest version of MongoDB using the [official MongoDB manual](https://docs.mongodb.com/manual/administration/install-community/). After installation is complete, copy the files from the `C:\Program Files\MongoDB\Server\4.2\bin` folder to the `monkey\monkey_island\bin\mongodb folder`. Try to run the Monkey Island again and everything should work.

## Can I limit how the Infection Monkey propagates through my network?

In order to limit how the Infection Monkey is able to propagate through your network, you can:

#### Adjust the scan depth

The scan depth limits the number of hops that the Infection Monkey agent will spread from patient zero. If
the scan depth is set to 1, the agent will spread only 1 hop from patient zero. Scan depth does not limit the number of
devices, just the number of hops.

- **Example**: Scan depth is set to 2. _Host A_ scans the network and finds hosts _B, C, D_ and _E_.
The Infection Monkey agent successfully propagates from _Host A_ to _Host C_. Since the scan depth is 2, the agent will pivot
from _Host C_ and continue to scan other machines on the network. If _Host C_ successfully breaches
_Host E_, it will not pivot further and it will not continue to scan or propagate.

![What is scan depth](/images/faq/propagation_depth_diagram.png "What is scan depth")


#### Enable/disable scanning the local subnet
Settings that define how the Infection Monkey will scan the network can be found in `Configuration -> Network`. By default each agent will scan its entire local subnet.
This behavior can be disabled by unchecking the `Local network scan` button.

#### Add IPs to the IP allow list

The Infection Monkey agents attempt to scan any hosts that are specified in the `Configuration -> Network -> Scan target list` section.

#### Add IPs to the IP block list

If there are any hosts on your network that you would like to prevent the Infection Monkey from scanning or exploiting, they can be added to list of "Blocked IPs" in `Configuration -> Network -> Blocked IPs`.

#### Specify max number of victims to find/exploit

Two settings in `Configuration -> Internal -> Monkey` allow you to further limit the Infection Monkey's propagation:

- **Max victims to find**: This limits the total number of machines that the Infection Monkey is allowed to scan.
- **Max victims to exploit**: This limits the number of machines that the Infection Monkey is allowed to successfully exploit.


## How can I get involved with the project?

Infection Monkey is an open-source project, and we welcome contributions and contributors. Check out the [contribution documentation]({{< ref "/development" >}}) for more information.

## About the project 🐵

### How did you come up with the Infection Monkey?

Oddly enough, the idea of proactively breaking a network to test its survival wasn't born in the security industry. In 2011, the streaming giant Netflix released Chaos Monkey, a tool designed to randomly disable the company's production servers to verify that they could survive network failures without any customer impact. Netflix's Chaos Monkey became a popular network resilience tool, breaking the network in a variety of failure modes, including connectivity issues, invalid SSL certificates and randomly deleting VMs.

Inspired by this concept, Guardicore Labs developed its own attack simulator - the Infection Monkey - to run non-intrusively within existing production environments. The idea was to test the resiliency of modern data centers against attacks and give security teams the insights they need to make informed decisions and enforce tighter security policies. Since its launch in 2017, the Infection Monkey has been used by hundreds of information technology teams from across the world to find weaknesses in their on-premises and cloud-based data centers.
