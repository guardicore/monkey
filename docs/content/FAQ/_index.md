---
title: "FAQ"
date: 2020-06-18T15:11:52+03:00
draft: false
pre: "<i class='fas fa-question'></i> "
---

Below are some of the most common questions we receive about the Infection Monkey. If the answer you're looking for isn't here, talk with us [on our Slack channel](https://infectionmonkey.slack.com/join/shared_invite/enQtNDU5MjAxMjg1MjU1LWM0NjVmNWE2ZTMzYzAxOWJiYmMxMzU0NWU3NmUxYjcyNjk0YWY2MDkwODk4NGMyNDU4NzA4MDljOWNmZWViNDU), email us at [support@infectionmonkey.com](mailto:support@infectionmonkey.com) or [open an issue on GitHub](https://github.com/guardicore/monkey).

- [Where can I get the latest version of the Infection Monkey?](#where-can-i-get-the-latest-version-of-the-infection-monkey)
- [I updated to a new version of the Infection Monkey and I'm being asked to delete my existing data directory. Why?](#i-updated-to-a-new-version-of-the-infection-monkey-and-im-being-asked-to-delete-my-existing-data-directory-why)
- [How can I use an old data directory?](#how-can-i-use-an-old-data-directory)
- [How long does a single Infection Monkey Agent run? Is there a time limit?](#how-long-does-a-single-infection-monkey-agent-run-is-there-a-time-limit)
- [How long does it take to stop all running Infection Monkey Agents?](#how-long-does-it-take-to-stop-all-running-infection-monkey-agents)
- [Is the Infection Monkey a malware/virus?](#is-the-infection-monkey-a-malwarevirus)
- [How do I reset the Monkey Island password?](#how-do-i-reset-the-monkey-island-password)
- [Should I run the Infection Monkey continuously?](#should-i-run-the-infection-monkey-continuously)
  - [Exactly what internet queries does the Infection Monkey perform?](#exactly-what-internet-queries-does-the-infection-monkey-perform)
- [Logging and how to find logs](#logging-and-how-to-find-logs)
  - [Downloading logs](#downloading-logs)
  - [Log locations](#log-locations)
  - [Monkey Island Server logs](#monkey-island-server-logs)
  - [Monkey Island UI logs](#monkey-island-ui-logs)
  - [Infection Monkey Agent logs](#infection-monkey-agent-logs)
- [Running the Infection Monkey in a production environment](#running-the-infection-monkey-in-a-production-environment)
  - [How much of a footprint does the Infection Monkey leave?](#how-much-of-a-footprint-does-the-infection-monkey-leave)
  - [What's the Infection Monkey Agent's impact on system resources usage?](#whats-the-infection-monkey-agents-impact-on-system-resources-usage)
  - [What are the system resource requirements for the Monkey Island?](#what-are-the-system-resource-requirements-for-the-monkey-island)
  - [Is it safe to use real passwords and usernames in the Infection Monkey's configuration?](#is-it-safe-to-use-real-passwords-and-usernames-in-the-infection-monkeys-configuration)
  - [How do you store sensitive information on Monkey Island?](#how-do-you-store-sensitive-information-on-monkey-island)
  - [How stable are the exploits used by the Infection Monkey? Will the Infection Monkey crash my systems with its exploits?](#how-stable-are-the-exploits-used-by-the-infection-monkey-will-the-infection-monkey-crash-my-systems-with-its-exploits)
- [After I've set up Monkey Island, how can I execute the Infection Monkey Agent?](#after-ive-set-up-monkey-island-how-can-i-execute-the-infection-monkey-agent)
- [How can I make the Infection Monkey Agents propagate "deeper" into the network?](#how-can-i-make-the-infection-monkey-agent-propagate-deeper-into-the-network)
- [Can I limit how the Infection Monkey propagates through my network?](#can-i-limit-how-the-infection-monkey-propagates-through-my-network)
- [How can I get involved with the project?](#how-can-i-get-involved-with-the-project)

## Where can I get the latest version of the Infection Monkey?

For the latest **stable** release, visit [our downloads
page](https://github.com/guardicore/monkey/releases/latest). **This is the
recommended and supported version**!

If you want to see what has changed between versions, refer to the [releases page on GitHub](https://github.com/guardicore/monkey/releases). For the latest development version, visit the [develop version on GitHub](https://github.com/guardicore/monkey/tree/develop).

## I updated to a new version of the Infection Monkey and I'm being asked to delete my existing data directory. Why?

The [data directory]({{< ref "/reference/data_directory" >}}) contains the
Infection Monkey's database and other internal
data. For the new version of Infection Monkey to work flawlessly, a data
directory with a compatible structure needs to be set up.

If you would like to save the data gathered from the Monkey's previous runs,
you can make a backup of your [existing data directory]({{< ref
"/reference/data_directory" >}}) before deleting it.

## How can I use an old data directory?

To use the data stored in a data directory from an older version, reinstall the
version of the Monkey Island which matches your data directory's version. Then,
copy the backup of your old data directory to the [appropriate location]({{<
ref "/reference/data_directory" >}}).

## How long does a single Infection Monkey Agent run? Is there a time limit?

The Infection Monkey Agent shuts off either when it can't find new victims or it has exceeded the quota of victims as defined in the configuration.

## How long does it take to stop all running Infection Monkey Agents?

On the Infection Map page, when <b>Kill All Monkeys</b> is pressed, the Agents
try to finish execution safely. This can take up to 2 minutes, but will be much
shorter on average.

## Is the Infection Monkey a malware/virus?

The Infection Monkey is not malware, but it uses similar techniques to safely
simulate malware on your network.

Because of this, the Infection Monkey gets flagged as malware by some antivirus
solutions during installation. If this happens, [verify the integrity of the
downloaded installer](/usage/file-checksums) first. Then, create a new folder
and disable antivirus scan for that folder. Lastly, re-install the Infection
Monkey in the newly created folder.

## How do I reset the Monkey Island password?

In order to reset the Monkey Island password, you'll need to [perform a factory
reset](/howtos/factory-reset).

## Should I run the Infection Monkey continuously?

Yes! This will allow you to verify that the Infection Monkey identified no new security issues since the last time you ran it.

## Does the Infection Monkey require a connection to the internet?

The Infection Monkey does not require internet access to function.

If internet access is available, the Infection Monkey will use the internet for two purposes:

- To check for updates.
- To check if machines can reach the internet.

### Exactly what internet queries does the Infection Monkey perform?

1. While the Monkey Island Server is being set up, a GET request with the deployment
type and version number is sent to the analytics server. This information is
collected to understand which deployment types and versions are no longer used
and can be deprecated.

1. After the Monkey Island starts, a GET request with the deployment type
is sent to the update server to fetch the latest version number and a
download link for it. This information is used by the Monkey Island to
suggest an update if one is available.

1. When you install a plugin it is downloaded from our official repository.

## Logging and how to find logs

### Downloading logs

Both the Agent and Island logs can be downloaded from the Infection Map page. See [how
to download logs](../howtos/download-logs) for more information.

### Log locations

See the [logs reference page](../reference/logs).


## Running the Infection Monkey in a production environment

### How much of a footprint does the Infection Monkey leave?

The Infection Monkey leaves hardly any trace on the target system. It will leave:

- Log files in [temporary directories]({{< ref "/faq/#infection-monkey-agent-logs">}}):
  - Path on Linux: `/tmp/infection-monky-agent-<TIMESTAMP>-<RANDOM_STRING>.log`
  - Path on Windows: `%temp%\\infection-monky-agent-<TIMESTAMP>-<RANDOM_STRING>.log`

### What's the Infection Monkey Agent's impact on system resources usage?

The Infection Monkey Agent uses less than a single-digit percent of CPU time and very low RAM usage. For example, on a single-core Windows Server machine, the Infection Monkey Agent consistently uses 0.06% CPU, less than 80MB of RAM and a small amount of I/O periodically.

If you do experience any performance issues please let us know on [our Slack channel](https://infectionmonkey.slack.com/) or [open an issue on GitHub](https://github.com/guardicore/monkey).

### What are the system resource requirements for the Monkey Island?

#### Linux

**CPU**: Intel(R) Xeon(R) CPU @ 2.20GHz or better

**CPU Cores**: 2

**RAM**: 4GB

#### Windows

**CPU**: Intel(R) Xeon(R) CPU @ 2.20GHz or better

**CPU Cores**: 4

**RAM**: 6GB

### Is it safe to use real passwords and usernames in the Infection Monkey's configuration?

Absolutely! User credentials are stored encrypted in the Monkey Island Server.
This information can only be seen by individuals that have the credentials to
access the Monkey Island.

### How do you store sensitive information on Monkey Island?

Sensitive data such as passwords, SSH keys and hashes are stored on the Monkey Island's database in an encrypted fashion. This data is transmitted to the Infection Monkey Agents in an encrypted fashion (HTTPS) and is not stored locally on victim machines.

When you reset the Monkey Island configuration, the Monkey Island wipes the information.

### How stable are the exploits used by the Infection Monkey? Will the Infection Monkey crash my systems with its exploits?

The Infection Monkey does not use any exploits or attacks that may impact the victim system.

This means we avoid using some powerful (and famous) exploits such as [EternalBlue](https://www.guardicore.com/2017/05/detecting-mitigating-wannacry-copycat-attacks-using-guardicore-centra-platform/). This exploit was used in WannaCry and NotPetya with huge impact, but, because it may crash a production system, we aren't using it.

## After I've set up Monkey Island, how can I execute the Infection Monkey Agent?

See our detailed [getting started]({{< ref "/usage/getting-started" >}}) guide.

## How can I make the Infection Monkey Agent propagate "deeper" into the network?

If you wish to simulate a very "deep" attack into your network, you can increase the *Maximum scan depth* parameter in the configuration. This parameter tells the Infection Monkey how far to propagate into your network from the "patient zero" machine.

To do this, change the `Configuration -> Propagation -> General -> Maximum scan depth` configuration option:

![How to increase propagation depth](/images/island/configuration_page/max_scan_depth_configuration.png "How to increase propagation depth")


## Can I limit how the Infection Monkey propagates through my network?

Yes! To limit how the Infection Monkey propagates through your network, you can:

#### Adjust the scan depth

The scan depth limits the number of hops that the Infection Monkey Agent will
spread from patient zero. If you set the scan depth to one, the Agent will only
reach a single hop from the initially infected machine. Scan depth does not
limit the number of devices, just the number of hops.

- **Example**: In this example, the scan depth is set to two. _Host A_ scans the
network and finds hosts _B, C, D_ and _E_. The Infection Monkey Agent
successfully propagates from _Host A_ to _Host C_. Since the scan depth is 2,
the Agent will pivot from _Host C_ and continue to scan other machines on the
network. However, if _Host C_ successfully breaches _Host E_, it will not pivot
further nor continue to scan or propagate.

![What is scan depth](/images/island/others/propagation_depth_diagram.png "What is scan
depth")

#### Enable or disable scanning the local subnet

You can find the settings that define how the Infection Monkey will scan your
network in `Configuration -> Propagation -> Network analysis`. If enabled,
the `Scan Agent's networks` setting instructs an Agent to scan its entire local subnet.

#### Add IPs to the IP allow list

You can specify which hosts you want the Infection Monkey Agents to attempt to
scan in the `Configuration -> Propagation -> Network analysis -> Scan target list` section.

#### Add IPs to the IP block list

If there are any hosts on your network that you would like to prevent the
Infection Monkey from scanning or exploiting, you can add them to the list of
"Blocked IPs" in `Configuration -> Propagation -> Network analysis -> Blocked IPs`.


## How can I get involved with the project?

Infection Monkey is an open-source project, and we welcome contributions and contributors. Check out the [contribution documentation]({{< ref "/development" >}}) for more information.

## About the project 🐵

### How did you come up with the Infection Monkey?

Oddly enough, the idea of proactively breaking a network to test its survival wasn't born in the security industry. In 2011, the streaming giant Netflix released Chaos Monkey, a tool designed to randomly disable the company's production servers to verify that they could survive network failures without any customer impact. Netflix's Chaos Monkey became a popular network resilience tool, breaking the network in a variety of failure modes, including connectivity issues, invalid SSL certificates and randomly deleting VMs.

Inspired by this concept, Guardicore Labs developed its own attack simulator - the Infection Monkey - to run non-intrusively within existing production environments. The idea was to test the resiliency of modern data centers against attacks and give security teams the insights they need to make informed decisions and enforce tighter security policies. Since its launch in 2017, the Infection Monkey has been used by hundreds of information technology teams from across the world to find weaknesses in their on-premises and cloud-based data centers.
