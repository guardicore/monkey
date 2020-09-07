---
title: "FAQ"
date: 2020-06-18T15:11:52+03:00
draft: false
pre: "<i class='fas fa-question'></i> "
---

Here are some of the most common questions we receive about the Infection Monkey. If the answer you’re looking for isn’t here, talk with us [on our Slack channel](https://infectionmonkey.slack.com/), email us at [support@infectionmonkey.com](mailto:support@infectionmonkey.com) or [open an issue on GitHub](https://github.com/guardicore/monkey).

- [Where can I get the latest Monkey version? 📰](#where-can-i-get-the-latest-monkey-version)
- [How long does a single Monkey run for? Is there a time limit?](#how-long-does-a-single-monkey-run-for-is-there-a-time-limit)
- [Should I run the Monkey continuously?](#should-i-run-the-monkey-continuously)
  - [Which queries does Monkey perform to the Internet exactly?](#which-queries-does-monkey-perform-to-the-internet-exactly)
- [Where can I find the log files of the Monkey and the Monkey Island, and how can I read them?](#where-can-i-find-the-log-files-of-the-monkey-and-the-monkey-island-and-how-can-i-read-them)
  - [Monkey Island](#monkey-island)
  - [Monkey agent](#monkey-agent)
- [Running the Monkey in a production environment](#running-the-monkey-in-a-production-environment)
  - [How much of a footprint does the Monkey leave?](#how-much-of-a-footprint-does-the-monkey-leave)
  - [What’s the Monkey’s impact on system resources usage?](#whats-the-monkeys-impact-on-system-resources-usage)
  - [Is it safe to use real passwords and usernames in the Monkey’s configuration?](#is-it-safe-to-use-real-passwords-and-usernames-in-the-monkeys-configuration)
  - [How do you store sensitive information on Monkey Island?](#how-do-you-store-sensitive-information-on-monkey-island)
  - [How stable are the exploitations used by the Monkey? Will the Monkey crash my systems with its exploits?](#how-stable-are-the-exploitations-used-by-the-monkey-will-the-monkey-crash-my-systems-with-its-exploits)
- [After I’ve set up Monkey Island, how can I execute the Monkey?](#after-ive-set-up-monkey-island-how-can-i-execute-the-monkey)
- [How can I make the monkey propagate “deeper” into the network?](#how-can-i-make-the-monkey-propagate-deeper-into-the-network)
- [The report returns a blank screen](#the-report-returns-a-blank-screen)
- [How can I get involved with the project? 👩‍💻👨‍💻](#how-can-i-get-involved-with-the-project)

## Where can I get the latest Monkey version? 📰

For the latest **stable** release for users, visit [our downloads page](https://www.guardicore.com/infectionmonkey/#download). **This is the recommended and supported version**!

If you want to see what has changed between versions, refer to the [releases page on GitHub](https://github.com/guardicore/monkey/releases). For the latest development version, visit the [develop version on GitHub](https://github.com/guardicore/monkey/tree/develop).

## How long does a single Monkey run for? Is there a time limit?

The Monkey shuts off either when it can't find new victims, or when it has exceeded the quota of victims as defined in the configuration.

## Should I run the Monkey continuously?

Yes! This will allow you to verify that no new security issues were identified by the Monkey since the last time you ran it.

Does the Infection Monkey require a connection to the Internet?

The Infection Monkey does not require internet access to function.

If internet access is available, the Monkey will use the Internet for two purposes:

- To check for updates.
- To check if machines can reach the internet.

### Which queries does Monkey perform to the Internet exactly?

The Monkey performs queries out to the Internet on two separate occasions:

1. The Infection Monkey agent checks if it has internet access by performing requests to pre-configured domains. By default, these domains are `updates.infectionmonkey.com` and `www.google.com`. The request doesn't include any extra information - it's a GET request with no extra parameters. Since the Infection Monkey is 100% open-source, you can find the domains in the configuration [here](https://github.com/guardicore/monkey/blob/85c70a3e7125217c45c751d89205e95985b279eb/monkey/infection_monkey/config.py#L152) and the code that performs the internet check [here](https://github.com/guardicore/monkey/blob/85c70a3e7125217c45c751d89205e95985b279eb/monkey/infection_monkey/network/info.py#L123). This **IS NOT** used for statistics collection.
1. After installation of the Monkey Island, the Monkey Island sends a request to check for updates. The request doesn't include any PII other than the IP address of the request. It also includes the server's deployment type (e.g. Windows Server, Debian Package, AWS Marketplace, etc.) and the server's version (e.g. "1.6.3"), so we can check if we have an update available for this type of deployment. Since the Infection Monkey is 100% open-source, you can inspect the code that performs this [here](https://github.com/guardicore/monkey/blob/85c70a3e7125217c45c751d89205e95985b279eb/monkey/monkey_island/cc/services/version_update.py#L37). This **IS** used for statistics collection. However due to the anonymous nature of this data we use this to get an aggregate assumption as to how many deployments we see over a specific time period - no "personal" tracking.

## Where can I find the log files of the Monkey and the Monkey Island, and how can I read them?

### Monkey Island

The Monkey Island’s log file can be downloaded directly from the UI. Click the “log” section and choose “Download Monkey Island internal logfile”, like so:

![How to download Monkey Island internal log file](/images/faq/download_log_monkey_island.png "How to download Monkey Island internal log file")

It can also be found as a local file on the Monkey Island server, where the Monkey Island was executed, called `info.log`.

The log enables you to see which requests were requested from the server, and extra logs from the backend logic. The log will contain entries like these ones for example:

```log
2019-07-23 10:52:23,927 - wsgi.py:374 -       _log() - INFO - 200 GET /api/local-monkey (10.15.1.75) 17.54ms
2019-07-23 10:52:23,989 - client_run.py:23 -        get() - INFO - Monkey is not running
2019-07-23 10:52:24,027 - report.py:580 - get_domain_issues() - INFO - Domain issues generated for reporting
```

### Monkey agent

The Monkey log file can be found in the following paths on machines where it was executed:

- Path on Linux: `/tmp/user-1563`
- Path on Windows: `%temp%\\~df1563.tmp`

The logs contain information about the internals of the Monkey’s execution. The log will contain entries like these ones for example:

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

## Running the Monkey in a production environment

### How much of a footprint does the Monkey leave?

The Monkey leaves hardly any trace on the target system. It will leave:

- Log files in the following locations:
  - Path on Linux: `/tmp/user-1563`
  - Path on Windows: `%temp%\\~df1563.tmp`

### What’s the Monkey’s impact on system resources usage?

The Infection Monkey uses less than single-digit percent of CPU time and very low RAM usage. For example, on a single-core Windows Server machine, the Monkey consistently uses 0.06% CPU, less than 80MB of RAM and a small amount of I/O periodically.

If you do experience any performance issues please let us know on [our Slack channel](https://infectionmonkey.slack.com/) or via [opening an issue on GitHub](https://github.com/guardicore/monkey).

### Is it safe to use real passwords and usernames in the Monkey’s configuration?

Absolutely! User credentials are stored encrypted in the Monkey Island server. This information is then accessible only to users that have access to the Island.

We advise to limit access to the Monkey Island server by following our [password protection guide](../usage/island/password-guide).

### How do you store sensitive information on Monkey Island?

Sensitive data such as passwords, SSH keys and hashes are stored on the Monkey Island’s database in an encrypted fashion. This data is transmitted to the Infection Monkeys in an encrypted fashion (HTTPS) and is not stored locally on the victim machines.

When you reset the Monkey Island configuration, the Monkey Island wipes the information.

### How stable are the exploitations used by the Monkey? Will the Monkey crash my systems with its exploits?

The Monkey does not use any exploits or attacks that may impact the victim system.

This means we avoid using some very strong (and famous) exploits such as [EternalBlue](https://www.guardicore.com/2017/05/detecting-mitigating-wannacry-copycat-attacks-using-guardicore-centra-platform/). This exploit was used in WannaCry and NotPetya with huge impact. But because it may crash a production system, we aren’t using it.

## After I’ve set up Monkey Island, how can I execute the Monkey?

See our detailed [getting started](../content/usage/getting-started) guide.

## How can I make the monkey propagate “deeper” into the network?

If you wish to simulate a very “deep” attack into your network, you can try to increase the *propagation depth* parameter in the configuration. This parameter tells the Monkey how far to propagate into your network from the “patient zero” machine in which it was launched manually.

To do this, change the “Distance from Island” parameter in the “Basic - Network” tab of the configuration:

![How to increase propagation depth](/images/faq/prop_depth.png "How to increase propagation depth")

## The report returns a blank screen

This is sometimes caused when Monkey Island is installed with an old version of MongoDB. Make sure your MongoDB version is up to date using the `mongod --version` command on Linux or the `mongod -version` command on Windows. If your version is older than **4.0.10**, this might be the problem. To update your Mongo version:

- **Linux**: First, uninstall the current version with `sudo apt uninstall mongodb` and then install the latest version using the [official mongodb manual](https://docs.mongodb.com/manual/administration/install-community/).
- **Windows**: First, remove the MongoDB binaries from the `monkey\monkey_island\bin\mongodb` folder. Download and install the latest version of mongodb using the [official mongodb manual](https://docs.mongodb.com/manual/administration/install-community/). After installation is complete, copy the files from the `C:\Program Files\MongoDB\Server\4.2\bin` folder to the `monkey\monkey_island\bin\mongodb folder`. Try to run the Island again and everything should work.

## How can I get involved with the project? 👩‍💻👨‍💻

The Monkey is an open-source project, and we weclome contributions and contributors. Check out the [contribution documentation](../development) for more information.

## About the project 🐵

### How did you come up with the Infection Monkey?

Oddly enough, the idea of proactively breaking the network to test its survival wasn’t born in the security industry. In 2011, the streaming giant Netflix released Chaos Monkey, a tool that was designed to randomly disable the company’s production servers to verify they could survive network failures without any customer impact. Netflix's Chaos Monkey became a popular network resilience tool, breaking the network in a variety of failure modes, including connectivity issues, invalid SSL certificates and randomly deleting VMs.

Inspired by this concept, Guardicore Labs developed its own attack simulator - Infection Monkey - to run non-intrusively within existing production environments. The idea was to test the resiliency of modern data centers against attack and give security teams the insights they need to make informed decisions and enforce tighter security policies. Since its launch in 2017 (?) the Infection Monkey has been used by hundreds of information technology teams from across the world to find weaknesses in their on-premises and cloud-based data centers.
