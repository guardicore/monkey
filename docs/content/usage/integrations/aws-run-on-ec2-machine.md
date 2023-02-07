---
title: "Running the Agent on AWS EC2 instances"
date: 2020-06-28T10:44:05+03:00
draft: false
description: "Use AWS SSM to execute Infection Monkey on your AWS instances."
tags: ["aws", "integration"]
---

## When to use this feature

This feature allows execution of the Infection Monkey Agent on EC2 instances with the help of an SSM agent.

Alternatively, you can execute a command on an EC2 instance manually (see [running manually](../../running-manually)) or using other management tools.

![AWS EC2 logo](/images/island/integrations/aws/aws-ec2.svg?height=250px "AWS EC2 logo")

## Setup

Assuming your network is already set up in AWS EC2, follow the steps below to get up and running quickly.

### Monkey Island deployment

In order to run the Infection Monkey Agents directly from the Monkey Island Server, you need to deploy the Monkey Island Server to an AWS EC2 instance in the same network which you want to test. For information about deploying the Monkey Island Server, see [setup](../../../setup).

### Setup IAM roles

In order for the Infection Monkey to successfully view your instances, you'll need to set appropriate IAM roles for your instances. You can read more about IAM roles [in Amazon's documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html), but it's not necessary in order to follow this setup.

#### Creating a custom IAM role

Go to the [AWS IAM roles dashboard](https://console.aws.amazon.com/iam/home?#/roles) and create a new IAM role for EC2. The role will need to have some specific permissions (see Appendix A), but you can just create a role with the `AmazonSSMManagedInstanceCore` and `AmazonSSMFullAccess` pre-made permissions. In the end it should look something like this:

![Creating a custom IAM role](/images/island/integrations/aws/monkey-island-aws-screenshot-3.png "Creating a custom IAM role")

#### Applying the IAM role to an instance

For each instance you'd like to access from the Monkey Island, apply the new IAM role you've just created to the instance. For example:

![Applying a custom IAM role](/images/island/integrations/aws/monkey-island-aws-screenshot-4.png "Applying a custom IAM role")

After applying the IAM role you should see this screen:

![Applying a custom IAM role](/images/island/integrations/aws/monkey-island-aws-screenshot-5.png "Applying a custom IAM role")

**Note: after setting IAM roles, the roles might take a few minutes (up to 10 minutes sometimes) to effectively kick in.** This is how AWS works and is not related to the Infection Monkey implementation. See [this StackOverflow thread for more details.](https://stackoverflow.com/questions/20156043/how-long-should-i-wait-after-applying-an-aws-iam-policy-before-it-is-valid)

### Setup the SSM agent

If your EC2 instances don't have the _SSM agent_ installed, they will not be able to execute SSM commands, which means you won't see them in the AWS machines table on the Monkey Island. Generally speaking, most new EC2 instances should have SSM pre-installed. The SSM Agent is installed, by default, on Amazon Linux base AMIs dated 2017.09 and later, on Amazon Linux 2, Ubuntu Server 16.04 and Ubuntu Server 18.04 LTS AMIs.

See [Amazon's documentation about working with SSM agents](https://docs.aws.amazon.com/systems-manager/latest/userguide/ssm-agent.html) for more details on how to check if you have an SSM agent and how to manually install one if you don't yet have it.

### Firewall rules

Make sure that all machines that will run the Monkey Agent can access the Island(port 5000).

## Usage

### Running the Infection Monkey

When you run the Monkey Island on an AWS instance, the Island detects it's running on AWS and presents the following option on the _"Run Monkey"_ page:

![Running a Monkey on EC2 Instance](/images/island/integrations/aws/monkey-island-aws-screenshot-1.png "Running a Monkey on EC2 Instance")

After you click on **Run on AWS machine of your choice** you can choose one of the available instances as "patient zero" by:

1. Selecting the machines you'd like to run the Infection Monkey on
2. Clicking **Run on Selected Machines** — now watch the Infection Monkey go! 🐒

![Running a Monkey on EC2 Instance](/images/island/integrations/aws/monkey-island-aws-screenshot-2.png "Running a Monkey on EC2 Instance")

## Notes

- The machines that can use IAM roles and be listed MUST be internet connected (or you can set up a proxy for IAM). This is standard AWS practice and you can read about it (and about how to set up the required proxy machines) in the AWS IAM documentation.
- You can view the Infection Monkey in [the AWS marketplace](https://aws.amazon.com/marketplace/pp/B07B3J7K6D).

### Appendix A: Specific policy permissions required

The IAM role will need to have, at minimum, the following specific permissions:

#### For executing the Monkey on other machines - SSM

- `"ssm:SendCommand"`
- `"ssm:DescribeInstanceInformation"`
- `"ssm:GetCommandInvocation"`

Here's the policy of the IAM role, as a JSON object:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "ssm:SendCommand",
                "ssm:DescribeInstanceInformation",
                "ssm:GetCommandInvocation"
            ],
            "Resource": "*"
        }
    ]
}
```
