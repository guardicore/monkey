---
title: "Scenarios"
date: 2020-05-26T21:01:19+03:00
draft: true
weight: 2
---

In this page we show how you can use the Infection Monkey to simulate breach and attack scenarios as well as to share some cool tips and tricks you can use to up your Infection Monkey game. This page is aimed at both novice and experienced Monkey users. You can also refer to [our FAQ](../../faq) for more specific questions and answers.

Here are a few scenarios that can be replicated in your own environment by executing the Monkey from different locations within the network, or with some tweaks to the Monkey’s configuration.

{{% notice note %}}
No worries! The Monkey does not cause any permanent system modifications that impact security or operations. You will be able to track the Monkey using the log files it leaves in well defined locations. [See our FAQ for more details](../faq).
{{% /notice %}}

- [Your network has been breached via internet facing servers](#your-network-has-been-breached-via-internet-facing-servers)
  - [Simulate this scenario using the Monkey](#simulate-this-scenario-using-the-monkey)
- [You are the newest victim of a phishing fraud! 🎣](#you-are-the-newest-victim-of-a-phishing-fraud)
  - [Simulate this scenario using the Monkey](#simulate-this-scenario-using-the-monkey-1)
- [You want to test your network segmentation](#you-want-to-test-your-network-segmentation)
  - [Simulate this scenario using the Monkey](#simulate-this-scenario-using-the-monkey-2)
- [You want to verify your security solutions, procedures and teams are working as intended](#you-want-to-verify-your-security-solutions-procedures-and-teams-are-working-as-intended)
  - [Simulate this scenario using the Monkey](#simulate-this-scenario-using-the-monkey-3)
- [Other useful tips](#other-useful-tips)

## Your network has been breached via internet facing servers

Whether it was the [Hex-men campaign](https://www.guardicore.com/2017/12/beware-the-hex-men/) that hit your Internet-facing DB server, a [cryptomining operation that attacked your WordPress site](https://www.guardicore.com/2018/06/operation-prowli-traffic-manipulation-cryptocurrency-mining-2/) or any other malicious campaign – the attackers are now trying to go deeper into your network.

### Simulate this scenario using the Monkey

To simulate this breach scenario, execute the Infection Monkey on different machines that host  internet-facing services such as your web servers (Apache, Tomcat, NGINX…) or your VPN servers. To see how to execute the Monkey on these servers, [refer to this FAQ question](../../faq#after-ive-set-up-monkey-island-how-can-i-execute-the-monkey).

{{% notice tip %}}
If you want to simulate a very “deep” attack into your network, see our [configuration documentation](../configuration).
{{% /notice %}}

After executing the Monkey, evaluate the results of this simulation using the information in the Report page. There you will find a summary of the most important things the simulation has discovered, a detailed report of all the Monkey’s findings and more. You can also use the Infection Map to analyze the Monkey’s progress through the network, and to see each Monkey’s detailed telemetry and logs.

## You are the newest victim of a phishing fraud! 🎣

Almost everyone is prone to phishing attacks. Results of a successful phishing attempt can be **extremely costly** as demonstrated in our report [IResponse to IEncrypt](https://www.guardicore.com/2019/04/iresponse-to-iencrypt/).

This scenario begins in a section of the network which is a potential phishing spot. Phishing attacks target human users - as such, these types of attacks try to penetrate the network via a service an employee is using, such as an email with an attached malware or social media message with a link redirecting to a malicious website. These are just two examples of where and how an attacker may choose to launch their campaign.

### Simulate this scenario using the Monkey

To simulate the damage from a successful phishing attack using the Infection Monkey, choose machines in your network from potentially problematic group of machines, such as the laptop of one of your heavy email users or one of your strong IT users (think of people who are more likely to correspond with people outside of your organization).

- After setting up the Island add the users’ **real** credentials (usernames and passwords) to the Monkey’s configuration (Don’t worry, this sensitive data is not accessible and is not distributed or used in any way other than being sent to the monkeys, and can be easily eliminated by resetting the Monkey Island’s configuration). Now you can simulate an attacker attempting to probe deeper in the network with credentials “successfully” phished.
- You can configure these credentials for the Monkey as follows:
From the **“Basic - Credentials”** tab of the Island’s configuration, under the **“Exploit password list”** press the ‘+’ button and add the passwords you would like the Monkey to use. Do the same with usernames in the **“Exploit user list”**.

After supplying the Monkey with the passwords and usernames, execute the Monkey from the simulated “victim” machines. To do this, click “**2. Run Monkey**” from the left sidebar menu and choose “**Run on machine of your choice**”.

## You want to test your network segmentation

Segmentation is a method of creating secure zones in data centers and cloud deployments that allows companies to isolate workloads from one another and secure them individually, typically using policies. A useful way to test the effectiveness of your segmentation is to ensure that your network segments are properly separated, e,g, your Development is separated from your Production, your applications are separated from one another etc. "to security test is to verify that your network segmentation is configured properly. This way you make sure that even if a certain attacker has breached your defenses, it can’t move laterally from point A to point B.

[Segmentation is key](https://www.guardicore.com/use-cases/micro-segmentation/) to protecting your network, reducing the attack surface and minimizing the damage of a breach. The Monkey can help you test your segmentation settings with its cross-segment traffic testing feature.

### Simulate this scenario using the Monkey

As an example, the following configuration makes sure machines in the “10.0.0.0/24” segment (segment A) and the “11.0.0.2/32” segment (segment B) can’t communicate with each other, along with an additional machine in 13.37.41.50.

![How to configure network segmentation testing](/images/usage/scenarios/segmentation-config.png "How to configure network segmentation testing")

## You want to verify your security solutions, procedures and teams are working as intended

The Infection Monkey can help you verify that your security solutions are working the way you expected them to. These may include your IR and SOC teams, your SIEM, your firewall, your endpoint security solution, and more.

### Simulate this scenario using the Monkey

Run the Monkey with whichever configuration you prefer. The default is good enough for many cases; but for example, you can add some old users and passwords. Running the Monkey on both the Island and on a few other machines in the network is also recommended, as it increases coverage and propagation rates.

After running the Monkey, follow the Monkeys’ actions on the Monkey Island’s infection map.

Now you can match this activity from the Monkey timeline display to your internal SIEM and make sure your security solutions are identifying and correctly alerting on different attacks.

- The red arrows indicate successful exploitations. If you see red arrows, those incidents ought to be reported as exploitation attempts, so check whether you are receiving alerts from your security systems as expected.
- The orange arrows indicate scanning activity, usually used by attackers to locate potential vulnerabilities. If you see orange arrows, those incidents ought to be reported as scanning attempts (and possibly as segmentation violations).
- The blue arrows indicate tunneling activity, usually used by attackers to infiltrate “protected” networks from the Internet. Perhaps someone is trying to bypass your firewall to gain access to a protected service in your network? Check if your micro-segmentation / firewall solution identify or report anything.

While running this scenario, be on the lookout for the action that should arise: Did you get a phone call telling you about suspicious activity inside your network? Are events flowing into your security events aggregators? Are you getting emails from your IR teams? Is the endpoint protection software you installed on machines in the network reporting on anything? Are your compliance scanners detecting anything wrong?

## Other useful tips

Here are a few tips which can help you push the Infection Monkey even further:

- Make sure the Monkey is configured to scan its local network but in addition, configure it with specific targets. To add these targets, add their IP addresses (or the IP ranges in which they reside) to the Scan IP/subnet list using the `+` button. Here’s an example of how this is achieved:

![How to configure Scan IP/subnet list](/images/usage/scenarios/scan-list-config.png "How to configure Scan IP/subnet list")

- Every network has its old “skeleton keys” that should have long been discarded. Configure the Monkey with old and stale passwords, but make sure that they were really discarded using the Monkey. To add the old passwords, in the island’s configuration, go to the “Exploit password list” under “Basic - Credentials” and use the “+” button to add the old passwords to the configuration. For example, here we added a few extra passwords (and a username as well) to the configuration:

![Exploit password and user lists](/images/usage/scenarios/user-password-lists.png "Exploit password and user lists")

- To see the Monkey executing in real-time on your servers, add the **post-breach action** command: `wall “Infection Monkey was here”`. This post breach command will broadcast a message across all open terminals on the servers the Monkey breached, to achieve the following: Let you know the Monkey ran successfully on the server. let you follow the breach “live” alongside the infection map, and check which terminals are logged and monitored inside your network. See below:

![How to configure post breach commands](/images/usage/scenarios/pba-example.png "How to configure post breach commands.")
