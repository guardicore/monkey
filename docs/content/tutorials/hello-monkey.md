---
title: "Tutorial 1: Hello, Monkey"
date: 2020-05-26T20:57:10+03:00
draft: false
pre: '<i class="fab fa-graduation-cap"></i> '
weight: 2
tags: ["tutorials", "hello-monkey"]
---

In this tutorial, we will use Infection Monkey to perform a brute-force SSH exploitation on a vulnerable container.


### Prerequisites

First, make sure that you have the following installed:
- `docker` and `docker-compose`


### Run the environment

Download the following `docker-compose.yml` file: [docker-compose.yml](https://raw.githubusercontent.com/guardicore/monkey-island/main/docker-compose.yml)

Then, navigate to the directory where you downloaded the file and run the following command to start the environment:

```
docker compose up
```

Now you should have 2 containers running:
- `monkey-island` - the Infection Monkey server
- `hello` - a vulnerable container

Now that the environment is running, open a browser to `https://localhost:5000` to access the Monkey Island web interface and create an account.

![Infection Monkey login screen](../../images/tutorials/hello-monkey/1-registration-page.jpg)
![Getting started page](../../images/tutorials/hello-monkey/2-getting-started-page.jpg)


### Scanning the vulnerable container

Select "Configure Monkey" on the "Getting Started" page (or select _Configuration_ in the navigation sidebar).

![Configuration page](../../images/tutorials/hello-monkey/3-configuration-page.jpg)

Navigate to the **Propagation** -> **Network analysis** section.

This is where the network scope of the simulation is defined. Our target container `hello` has a host name `hello`, so to target it add the host name to the target list as shown in the picture:

![Scan target list in the Network Analysis configuration](../../images/tutorials/hello-monkey/5-scan-target-list.jpg)

Scroll to the bottom of the page and click **Submit** in order to save the configuration.

Now lets run the Monkey Agent. Navigate to the **1. Run Monkey** page. Click the **From Island** button. This will run the Monkey agent inside the `monkey-island` container.

![Run Monkey page](../../images/tutorials/hello-monkey/7-run-monkey.jpg)

To see what is happening in the network navigate to the **2. Infection Map** page. You should see an arrow appear between the `monkey-island` container and the vulnerable container. The arrow indicates that the Monkey has scanned the container.

![Network map](../../images/tutorials/hello-monkey/8-map-scanned.jpg)

Click on the containers/arrows in the map to see more information about them. You can also navigate to the **3. Security Reports** page to see a more detailed report of what happened in the network.

![Exploit timeline](../../images/tutorials/hello-monkey/9-exploit-timeline.jpg)


### Exploiting the vulnerable container

Now that we know how to scan a machine we can look into exploiting it. In order to perform an SSH brute-force attack, we will need to install an SSH exploiter plugin.

Navigate to the **Plugins** page. Under the **Available Plugins** tab you'll see a list of all the plugins that can be installed. Find the **SSH** exploiter (not credentials collector) and click the download button to install it.

![Filtered plugin list](../../images/tutorials/hello-monkey/11-filtered-plugin-list.jpg)

Now that we have the SSH exploiter plugin we can configure it. Navigate to the **Configuration** page and select the **Propagation** -> **Exploiters** tab (opened by default). Enable the SSH exploiter and submit the configuration.

![Enable the SSH Exploiter](../../images/tutorials/hello-monkey/12-exploiter-enabled.jpg)

Even though the SSH exploiter is enabled the Monkey doesn't know what credentials to use for its brute-force attacks. To configure that navigate to the **Propagation** -> **Credentials** tab. Add a new credential with the identity `user` and the password `password`. Hit the **Save** button to save the entry and submit the configuration.

![Credentials saved](../../images/tutorials/hello-monkey/14-saved-credentials.jpg)

Now that we've configured the exploitation let's try running the Agent again. Navigate to **1. Run Monkey** and click on the **From Island** button. Then, navigate to the **2. Infection Map** page to observe the Monkey's progress.

What should happen on the map:

1. A yellow arrow should change to red, because after the scan the Agent on the `monkey-island` should successfully guess the SSH credentials and exploit the `hello` container.
2. The `hello` container icon should get a checkmark added on it. This means that the Monkey Agent was uploaded and ran there.
3. A gray arrow should appear between the `hello` and `monkey-island` containers. This means that the Agent was able to report back to the `monkey-island` container.

Once all agents finish running your map should look like this:

![Network map](../../images/tutorials/hello-monkey/15-map-exploited.jpg)

To see more details about what happened in the network you can inspect the **3. Security Reports** page.

### Next steps

Now that you know more about Infection Monkey you should be able to use it for more complex cases, like:

- Inspecting what an attacker would see in the network if he were to compromise a specific machine
- Seeing how your defensive solutions would react to a real-world attack
- Seeing if and how many credentials can be stolen from a machine
- Perform a reversable ransowmare attack to make sure it gets stopped and/or you can recover from it
- And many more!
