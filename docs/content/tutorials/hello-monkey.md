---
title: "Tutorial 1: Hello Monkey"
date: 2020-05-26T20:57:10+03:00
draft: false
pre: '<i class="fab fa-graduation-cap"></i> '
weight: 2
tags: ["tutorials", "hello-monkey"]
---

## Hello Monkey

Note: Build the docker container (run build.sh)
Note: What are the learning objectives?

In this tutorial, we will use the Infection Monkey to exploit a simple vulnerability. We will configure Infection Monkey to exploit the vulnerability, and then run the Monkey to observe that it is able to gain access to the machine. You'll learn how to start Infection Monkey, configure it, and run it.

### Prerequisites
First, make sure that you have the following prerequisites installed:
- `docker` and `docker-compose`

### Run the environment
Next, we'll use docker compose to run Infection Monkey along with our vulnerable container.

Run `docker compose up` to start the environment

{{% notice note %}}
The current docker compose script uses the host network.
{{% /notice %}}

Now that the environment is running, open a browser to `https://localhost:5000` to access the Monkey Island web interface. You will be presented with a registration page if you haven't registered. Provide a username and password to log in.

TODO: Screenshot of monkey login screen


### Configure the Monkey
Now we'll need to configure Infection Monkey to exploit the vulnerable container. Select "Configure Monkey" on the "Getting Started" page (or select _Configuration_ in the navigation sidebar).

Before the Monkey can do anything useful, it needs to be configured. Otherwise, it won't know what exploits to attempt, or what machine(s) to attempt to breach.

{{% notice note %}}
The Infection Monkey will only attempt to breach the machines that you've explicitly configured it to target.
{{% /notice %}}

#### Tell the Monkey what machines to target
In our case, we know that the target machine has the hostname `hello`. In order to tell the Monkey to target that hostname, starting from the **Configuration** page, ensure that **Propagation** tab is selected, and then select the **Network analysis** subtab. Then, under the "Scan target list" section, click the "+" button to add a target to scan. Enter our target hostname, `hello`, into the input field. Finally, make sure to scroll to the bottom and click **Submit** in order to save the configuration.

TODO: Screenshots of configuration page(s)


Great, the Monkey knows what machine to target. What happens if we run it? Select **1. Run Monkey** in the navigation sidebar to bring up the Run Monkey page. We'll choose the **From Island** option, which will start the Monkey from the Island machine.


#### Tell the Monkey what exploiters to use
- Install SSH Exploiter plugin
- Configure Username/Password for exploitation

### Run the Monkey
With the Monkey configured, all's that's left to do is run it!

TODO: Screenshot of the run page

{{% notice note %}}
Test
{{% /notice %}}

TODO: Screenshot of the map

{{% notice tip %}}
Test
{{% /notice %}}

### Next steps
- Secure the vulnerable machine and try again?
-
- ...
