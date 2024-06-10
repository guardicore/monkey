---
title: "Tutorial 2: Ransomware"
date: 2020-05-26T20:57:10+03:00
draft: false
pre: '<i class="fas fa-lock"></i> '
weight: 2
tags: ["tutorials", "ransomware"]
---

In this tutorial, we'll configure and run a ransomware simulation using
Infection Monkey. You'll learn:
- How to setup an environment for a ransomware scenario
- How to configure Infection Monkey to perform a ransomware attack
- How to observe the results of the ransomware attack

### Prerequisites
To complete this tutorial, you'll need to have the sandbox environment set up.
Follow the steps in [Tutorial 0: First steps](../first-steps) if you have not
done so already.

### Configure the vulnerable container
For this scenario, we're going to need some valuable data so that it can be
held for ransom. We'll create a directory named `vault`, and we'll add a list
of passwords to that vault.

Connect to the container:

```
docker exec -it --user user hello bash
```

Add a file named `passwords.txt`:
```
mkdir ~/vault
cat << EOF > ~/vault/passwords.txt
password
P@ssw0rd
supersecretpassword
EOF
```

Now let's see if we can get Infection Monkey to encrypt our data!

### Configure Infection Monkey

#### Install plugins
Our first task is to make sure we have the required plugins installed. In order
to exploit the vulnerable container, we'll need the SSH exploiter plugin. Then,
to run the ransomware simulation on the exploited container, we'll need the
ransomware plugin.

Navigate to the **Plugins** page by selecting _Plugins_ in the navigation
sidebar. You'll see a list of all the plugins that can be installed. Install
the _SSH Exploiter_ and _Ransomware Payload_ by clicking their respective
download icons in the right-most column of the table. You'll see the download
icons transform into check marks once installation is complete.

![Plugins page](../../images/tutorials/ransomware/010-plugin-installation.gif)

Now that the plugins have been installed, we're ready to configure our
simulation.

#### Tell the Monkey which exploiter to use
Navigate to the **Configuration** page by selecting _Configure Monkey_ on the
**Getting Started** page (or select _Configuration_ in the navigation sidebar).
Check the box next to the _SSH Exploiter_ to enable it.

![Enable the SSH
Exploiter](../../images/tutorials/ransomware/020-exploiter-enabled.jpg)

#### Tell the Monkey which machine to target
Switch to the **Network analysis** subtab and click the yellow _+_ button under
_Scan target list_. You'll see a new field appear. Enter the hostname of the
vulnerable container, `hello`, in the field.

![Scan target list in the Network Analysis
configuration](../../images/tutorials/ransomware/030-scan-target-list.jpg)

#### Tell the Monkey what credentials to use
The SSH exploiter needs one or more sets of credentials that it can use to
attempt to access the target host. Switch to the **Credentials** subtab and
enter `user` for _Identity_ and `password` for _Password_. Click the blue
_SAVE_ button or hit the enter key. You'll see the credentials you've added
appear below under _Saved credentials_.

![Credentials
entered](../../images/tutorials/ransomware/040-credentials-input.jpg)

#### Tell the Monkey to use the Ransomware plugin
Our final configuration step is to enable the ransomware plugin. Select the
**Payloads** tab at the top of the page and enable the _Ransomware_ plugin in
the _Enabled payloads_ list by checking the box next to it.

![Ransomware
enabled](../../images/tutorials/ransomware/050-ransomware-enabled.jpg)

Next, we'll need to tell the Ransomware plugin which directory to hold for
ransom. Since the `hello` container is linux-based, set the _Linux target
directory_ to `/home/user/vault` (the directory that we [prepared
earlier](#configure-the-vulnerable-container)).

{{% notice warning %}}
Infection Monkey will encrypt the contents of whichever directory we configure
it to target. Therefore, when setting up a ransomware scenario, target a
directory with dummy data or make sure you have a way to recover the data in
the target directory.
{{% /notice %}}


![Ransomware
configured](../../images/tutorials/ransomware/060-ransomware-configuration.jpg)

Make sure that _Leave ransom note_ is checked and click the green _Submit_
button at the bottom of the screen to save our configuration.

### Run Infection Monkey
Now that we've configured Infection Monkey, let's run it!

Go to the **Run Monkey** page by selecting _1. Run Monkey_ from the navigation
sidebar. Click the _From Island_ button to launch an attack on the vulnerable
container from the Monkey Island.

If you look at the **Infection Map**, you'll see that the `hello` container
gets exploited as it did in [Tutorial 1: Hello, Monkey](../hello-monkey).

You can tell that the run has completed when a check mark appears next to the
_Infection Map_ and _Security Report_ in the navigation sidebar:

![Infection Monkey run
completed](../../images/tutorials/ransomware/070-run-monkey.jpg)


Great! The run has completed, but how do we know whether or not our ransomware
succeeded?

One good place to look is the **Ransomware report**. Navigate to the **Security
Reports** page by selecting _3. Security reports_ on the navigation sidebar.
Select the **Ransomware report** tab and scroll down to take a look at the _3.
Attack_ section. It lists the files that Infection Monkey was able to encrypt:

![List of files taken for ransom in ransomware
report](../../images/tutorials/ransomware/080-ransomware-report.jpg)

It looks like our passwords are being held for ransom! Let's connect to the
container and observe the contents of the vault:
```
docker exec -it --user user hello bash

ls -1 ~/vault
```

We'll see two files:
```
README.txt
passwords.txt.m0nk3y
```

`README.txt` is the ransom note that Infection Monkey leaves in the directory
targeted by the Ransomware plugin. `passwords.txt.m0nk3y` is our password list
(formerly `passwords.txt`) that Infection Monkey encrypted. First, let's take a
peek at the ransom note:

```
$ cat ~/vault/README.txt
```

You should see
[this](https://raw.githubusercontent.com/guardicore/monkey/develop/monkey/agent_plugins/payloads/ransomware/src/ransomware_readme.txt)
printed to the console.

Next, let's print the contents of the encrypted password file to verify that
the file is indeed encrypted:

```shell
$ cat ~/vault/passwords.txt.m0nk3y
��������������ύ����������������������
```

Looks like the Monkey did its job!

{{% notice tip %}}
Infection Monkey uses a bit flip algorithm to "encrypt" files. So if you find
yourself in a situation where you need to reverse the encryption, you can drop
the file extension that the Monkey adds, and then re-run the ransomware
simulation. This will re-flip the bits, returning the files to their original
state.
{{% /notice %}}

### Review
In this tutorial, you have learned:
- Infection Monkey provides a ransomware plugin that enables you to simulate a
  ransomware attack.
- How to prepare systems for a ransomware simulation by deploying target files.
- How to configure Infection Monkey to use its ransomware plugin.
- How to view and interpret the results of Infection Monkey's ransomware report.

### Next Steps
- Try removing the extension that Infection Monkey adds to the encrypted file
  and re-running the ransomware simulation to "decrypt" the file.
- Try playing with the Ransomware plugin's configuration options.
- Read our [ransomware usage document](../../usage/ransomware-simulation).
