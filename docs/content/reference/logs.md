---
title: "Logs"
date: 2024-06-03T13:20:41-04:00
draft: false
pre: '<i class="fas fa-file-lines"></i> '
weight: 50
tags: ["logs", "reference"]
---

## Logs

### Agent

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
5. As a last resort, the current working directory (i.e. the directory from
   which the Agent was launched).

Infection Monkey log file name is constructed according to the following
pattern: `infection-monkey-agent-<TIMESTAMP>-<RANDOM_STRING>.log`


### Island

The Monkey Island's log file is named `monkey_island.log` and is located in the
[data directory]({{< ref "/reference/data_directory" >}}). This log shows the
requests sent to the Monkey Island server, as well as details about how data is
processed.

#### Next generation UI (development only)

The Monkey Island's UI produces a log file named `nextjs.log` located in the
[data directory]({{< ref "/reference/data_directory" >}}). This log contains
the output of the server process hosting the web interface.

### MongoDB

MongoDB's log file is named `mongodb.log` and is located in the
[data directory]({{< ref "/reference/data_directory" >}}).

### See also

- [Data directory reference]({{< ref "/reference/data_directory" >}})
- [How to download logs](../howtos/download_logs)
