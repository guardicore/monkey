---
title: "Tutorial 1: Hello, Monkey"
date: 2020-05-26T20:57:10+03:00
draft: false
pre: '<i class="fas fa-hand-spock"></i> '
weight: 2
tags: ["tutorials", "hello-monkey"]
---

In this tutorial, we will use Infection Monkey to exploit a simple
vulnerability. We will configure Infection Monkey to exploit the vulnerability
and target a specific machine, and then run it to observe that it is able to
gain access to the machine. You'll learn how to start Infection Monkey,
configure it, and run it against a network. Specifically, you'll learn how to:
- Install plugins
- Specify targets for Infection Monkey to exploit in the network
- Tell Infection Monkey what exploits to attempt against machines on the
  network
- Provide Infection Monkey with credentials that it can use when attempting to
  exploit machines
- Run the Monkey and observe its progress

### Prerequisites

To complete this tutorial, you'll need to have the sandbox environment set up.
Follow the steps in [Tutorial 0: First steps](../first-steps) if you have not
done so already.

### Configure the Monkey
Before the Monkey can do anything useful, it needs to be configured. Otherwise,
it won't know what exploits to attempt, or what machine(s) to attempt to
breach. To navigate to the **configuration** page, select _Configure Monkey_
on the **Getting Started** page (or select _Configuration_ in the navigation
sidebar).

![Configuration
page](../../images/tutorials/hello-monkey/3-configuration-page.jpg)

#### Tell the Monkey which machines to target
For this tutorial, we're going to configure the Monkey to exploit the
vulnerable container within the sandbox environment, which has the hostname
`hello`. In order to tell the Monkey to target that hostname, click the the
**Propagation** tab and then select the **Network analysis** subtab.

{{% notice note %}}
The Infection Monkey will only attempt to breach the machines that you've
explicitly configured it to target. This helps to ensure that the Monkey
doesn't run amok on your network.
{{% /notice %}}

![Network analysis
configuration](../../images/tutorials/hello-monkey/4-network-analysis.jpg)

Then, under the _Scan target list_ section, click the yellow _+_ button to add
a target to scan. You'll see a new field appear. Enter our target hostname,
`hello`, in the field.

![Scan target list in the Network Analysis
configuration](../../images/tutorials/hello-monkey/5-scan-target-list.jpg)

Finally, make sure to scroll to the bottom and click _Submit_ in order to
save the configuration. You should see a notice indicating that the
configuration was submitted successfully.

![Submit button](../../images/tutorials/hello-monkey/6-submit-button.jpg)

Great! The Monkey now knows which machine to target. What happens if we run it?
Select _1. Run Monkey_ in the navigation sidebar to bring up the Run Monkey
page. We'll choose the _From Island_ option, which will start the Monkey from
the Island machine. Go ahead and do that now.

![Run Monkey page](../../images/tutorials/hello-monkey/7-run-monkey.jpg)

Observe that a check mark appears next to _1. Run Monkey_ in the navigation
sidebar. This indicates that a Monkey Agent has started.

You can see the Monkey's progress by selecting _2. Infection Map_ in the
navigation sidebar. This brings up a network view (from the Monkey's
perspective). You should see an arrow appear between the `monkey-island`
machine and the vulnerable container. If you look at the legend, you'll notice
that this indicates that the Monkey scanned the container.

![Network map](../../images/tutorials/hello-monkey/8-map-scanned.jpg)

You should also observe a check mark appear next to both _2. Infection Map_
and _3. Security Reports_ in the navigation sidebar. This indicates that the
assessment has completed. Also note that while the Monkey was able to scan the
container, it was not able to exploit it. In fact, if you select the vulnerable
container in the infection map view, you'll see that it _hasn't even
attempted_ to exploit it. This is because we haven't configured the Monkey with
any exploiters. We'll do that next.

![Exploit timeline](../../images/tutorials/hello-monkey/9-exploit-timeline.jpg)


#### Tell the Monkey which exploiters to use
Now we're going to configure the Monkey to use an exploiter. In order to do
that, select _Configuration_ in the navigation sidebar. Select the
**Propagation** tab, and the **Exploiters** subtab. You should see a list of
_Enabled exploiters_, which you'll notice, is empty. This is because we haven't
installed any exploiters yet. Thankfully, the _Enabled exploiters_ list
provides a link to a page where we can download and install exploiter plugins,
so let's follow that link and install an exploiter.

![Empty exploiters
list](../../images/tutorials/hello-monkey/10-empty-exploiter-list.jpg)

{{% notice note %}}
Infection Monkey does not come with exploiters pre-installed. However, it
provides an easy way to download and install them from within the Island web
interface.
{{% /notice %}}

You should now be at the **Plugins** page. Under the **Available Plugins** tab
you'll see a list of all the plugins that can be installed. Infection Monkey
has several types of plugins. Since we're interested in installing an
exploiter, let's filter this list to only show us exploiters. Select the _Type_
dropdown, and choose _Exploiter_. You should now see that the _Type_ column
contains only "Exploiter".

For this tutorial we're going to install the _SSH Exploiter_. Type `ssh` into
the search field, and you should see an exploiter named "SSH". Click the
download button to install that exploiter. The button will change into a
loading indicator to show that it's installing, and then to a check mark when
the plugin is installed. You can go to the **Installed Plugins** tab and see
that a plugin named "SSH" of type "Exploiter" is installed.

![Filtered plugin
list](../../images/tutorials/hello-monkey/11-filtered-plugin-list.jpg)

Great! We've installed the SSH exploiter, but we still need to tell the Monkey
to use it. Navigate back to the **Configuration** page, and notice that the
_Enabled exploiters_ list now shows _SSH Exploiter_ as an option. Check the box
next to _SSH Exploiter_, leave the default option values unchanged, and then
**Submit** the configuration.

![Enable the SSH
exploiter](../../images/tutorials/hello-monkey/12-exploiter-enabled.jpg)


We've told Infection Monkey which exploiter to use, but we've still got one
more step: the SSH exploiter requires credentials in order to run, and we
haven't provided any. Let's do that now.

{{% notice note %}}
Brute force exploiters, such as the SSH exploiter, require credentials in order
to run.
{{% /notice %}}


#### Tell the Monkey which credentials to use
From the **Configuration** page, select the **Propagation** tab, then the
**Credentials** subtab.

Enter `user` into the _Identity_ field, and `password` in the _Password_
field. Click the blue _SAVE_ button or hit the enter key.

![Credentials
entered](../../images/tutorials/hello-monkey/13-credentials-input.jpg)

You will see a new entry appear in the _Saved Credentials_ list:

![Credentials
saved](../../images/tutorials/hello-monkey/14-saved-credentials.jpg)

Make sure you _Submit_ the configuration so that the credentials are saved.

Okay, let's give it one more go. Navigate to the **Run Monkey** page, and run
the Monkey **From Island**. Click the _From Island_ button to launch an attack
on the vulnerable container from the Monkey Island. Then, switch to the
**Infection Map** page and observe the Monkey's progress:

![Network map](../../images/tutorials/hello-monkey/15-map-exploited.jpg)

Huzzah! We've succeeded!

Notice how the arrow from the `monkey-island` to the vulnerable container
changed to red? That indicates that Infection Monkey successfully exploited the
container. The check mark on the container means that the Monkey Agent was
executed in the container, and the gray arrow from the container to the Island
indicates that the Monkey Agent reported back to the Island.


### Review
Let's take a moment to review what you've learned:
- You now know that the Monkey does not come with exploiters out of the box,
  but they can be installed easily. You also know how to get to the **Plugins**
  page and install plugins.
- You've learned how to tell the Monkey which machines to target, which
  exploiters to use, as well as how to provide credentials to the Monkey.
- You've learned how to run the Monkey and observe its progress.


### Next steps
Now that you're more familiar with Infection Monkey, you might try the
following:

- Secure the vulnerable machine and run the Monkey to verify that the machine
  can no longer be exploited.
- Explore some of the other configuration options.
- Simulate a network breach on a specific machine by [running the Monkey
  manually](../../usage/running-manually).
- Explore some of the other exploiter plugins.
- Use the Monkey to [simulate a ransomware attack](../ransomware).
