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
- [Reset the Monkey Island password](#reset-the-monkey-island-password)
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
- [What if the report returns a blank screen?](#what-if-the-report-returns-a-blank-screen)
- [Can I limit how the Infection Monkey propagates through my network?](#can-i-limit-how-the-infection-monkey-propagates-through-my-network)
- [How can I get involved with the project?](#how-can-i-get-involved-with-the-project)

## Where can I get the latest version of the Infection Monkey?

For the latest **stable** release, visit [our downloads page](https://www.akamai.com/infectionmonkey#download). **This is the recommended and supported version**!

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

## Reset the Monkey Island password

{{% notice warning %}}
If you reset the credentials, the database will be cleared. Any findings of the Infection Monkey from previous runs will be lost. <br/><br/>
However, you can save the Monkey's existing configuration by logging in with your current credentials and clicking on the **Export config** button on the configuration page.
{{% /notice %}}

### On Windows and Linux (AppImage)

When you first access the Monkey Island Server, you'll be prompted to create an account.
Creating an account will write your credentials to the database in the [data directory]({{< ref "/reference/data_directory" >}}).

To reset the credentials:

1. **Remove** the data directory manually

    Because credentials are stored in the database, you must perform a complete factory reset in order to reset the credentials, which is accomplished by removing the entire [data directory]({{< ref "/reference/data_directory" >}}).

2. Restart the Monkey Island process:
    * On Linux, simply kill the Monkey Island process and execute the AppImage.
    * On Windows, restart the program.

3. Go to the Monkey Island's URL and create a new account.

### On Docker
When you first access the Monkey Island Server, you'll be prompted to create an account.
To reset the credentials, you'll need to perform a complete factory reset:

1. Kill the Monkey Island container:
    ```bash
    sudo docker kill monkey-island
    ```
1. Kill the MongoDB container:
    ```bash
    sudo docker kill monkey-mongo
    ```
1. Remove the MongoDB volume:
    ```bash
    sudo docker volume rm db
    ```
1. Restart the MongoDB container:
   ```bash
    sudo docker run \
        --name monkey-mongo \
        --network=host \
        --volume db:/data/db \
        --detach \
        mongo:6.0
    ```
1. Restart the Monkey Island container
    ```bash
    sudo docker run \
        --name monkey-island \
        --network=host \
        infectionmonkey/monkey-island:latest
    ```
1. Go to the Monkey Island's URL and create a new account.


## Should I run the Infection Monkey continuously?

Yes! This will allow you to verify that the Infection Monkey identified no new security issues since the last time you ran it.

Does the Infection Monkey require a connection to the internet?

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

Both Monkey Agent and Monkey Island logs can be found in the Infection Map page. Click on the
machine from which you want to download logs and press the "Download log" button on the side panel.
Note that you can only download the Monkey Island log by clicking on the Monkey Island machine in
the Infection Map.

![How to download logs](/images/island/infection_map_page/agent_log_download.png "How to download logs")

### Log locations

If the logs cannot be downloaded through the UI for any reason, you can collect the log files
directly from the machine where an Agent or Monkey Island ran.

#### Monkey Island Server logs

The Monkey Island's log file is located in the
[data directory]({{< ref "/reference/data_directory" >}}).

The log enables you to see which requests were requested from the server and extra logs from the backend logic. The log will contain entries like these:

```log
2022-04-18 13:48:43,914 - pywsgi.py:1226 -      write() - INFO - 192.168.56.1 - - [2022-04-18 13:48:43] "GET /api/agent-binaries/windows HTTP/1.1" 200 21470665 0.293586
2022-04-18 13:48:49,970 - pywsgi.py:1226 -      write() - INFO - 192.168.56.1 - - [2022-04-18 13:48:49] "GET /api/island-mode HTTP/1.1" 200 128 0.003426
2022-04-18 13:48:49,988 - report.py:355 - get_domain_issues() - INFO - Domain issues generated for reporting
```

It's also possible to change the default log level by editing `log_level` value in a [server configuration file](../../reference/server_configuration).
`log_level` can be set to `info`(default, less verbose) or `debug`(more verbose).


#### Monkey Island UI logs

The Monkey Island's UI log file (`nextjs.log`) is located in the
[data directory]({{< ref "/reference/data_directory" >}}).

This log contains the output of the server process hosting the web interface.


#### Infection Monkey Agent logs

The Infection Monkey Agent log file can be found in directories specified for
temporary files on the machines where it was executed. In most cases, this will
be `/tmp` on Linux and `%temp%` on Windows. The Agent searches a standard list
of directories to find an appropriate place to store the log:

1. The directory named by the `TMPDIR` environment variable.
2. The directory named by the `TEMP` environment variable.
3. The directory named by the `TMP` environment variable.
4. A platform-specific location:
   - On Windows, the directories `C:\TEMP`, `C:\TMP`, `\TEMP`, and `\TMP`, in that order.
   - On all other platforms, the directories `/tmp`, `/var/tmp`, and `/usr/tmp`, in that order.
5. As a last resort, the current working directory.

Infection Monkey log file name is constructed to the following pattern: `infection-monkey-agent-<TIMESTAMP>-<RANDOM_STRING>.log`

The logs contain information about the internals of the Infection Monkey Agent's execution. The log will contain entries like these:

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

Absolutely! User credentials are stored encrypted in the Monkey Island Server. This information is accessible only to users that have access to the specific Monkey Island.

We advise users to limit access to the Monkey Island Server by following our [password protection guide]({{< ref "/setup/accounts-and-security" >}}).

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

## What if the report returns a blank screen?

This is sometimes caused when Monkey Island is installed with an old version of MongoDB. Make sure your MongoDB version is up to date using the `mongod --version` command on Linux or the `mongod -version` command on Windows. If your version is older than **4.0.10**, this might be the problem. To update your Mongo version:

- **Linux**: First, uninstall the current version with `sudo apt uninstall mongodb` and then install the latest version using the [official MongoDB manual](https://docs.mongodb.com/manual/administration/install-community/).
- **Windows**: First, remove the MongoDB binaries from the `monkey\monkey_island\bin\mongodb` folder. Download and install the latest version of MongoDB using the [official MongoDB manual](https://docs.mongodb.com/manual/administration/install-community/). After installation is complete, copy the files from the `C:\Program Files\MongoDB\Server\4.2\bin` folder to the `monkey\monkey_island\bin\mongodb folder`. Try to run the Monkey Island again and everything should work.

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
