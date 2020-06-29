---
title: "Running the monkey on AWS EC2 instances"
date: 2020-06-28T10:44:05+03:00
draft: false
description: "Use AWS SSM to execute Infection Monkey on your AWS instances."
tags: ["aws", "integration"]
---

## When to use this feature

If your network is deployed on Amazon Web Services (with EC2 instances), and you'd like to run the Infection Monkey in order to test it, this page is for you. You can easily run the monkey on **various instances** within your network - in a secure fashion, **without** feeding the Island with any credentials or running shell commands on the machines you want to test.

The results will be exported to AWS security hub automatically, as well. To see more information about that, see the [Infection Monkey and AWS Security Hub documentation](https://github.com/guardicore/monkey/wiki/Infection-Monkey-and-AWS-Security-Hub).

![AWS EC2 logo](/images/usage/integrations/aws-ec2.svg?height=250px "AWS EC2 logo")

## Setup

Assuming your network is already set up in AWS EC2, follow these quick steps to get up and running.

### Monkey Island deployment

In order to run the Monkeys directly from the Monkey Island server, you need to deploy the Monkey Island server to an AWS EC2 instance in the same network which you want to test. For information about deploying the Monkey Island server, see [setup](../../../setup).

### Setup IAM roles

In order for the Island to successfully view your instances, you'll need to set appropriate IAM roles to your instances. You can read more about IAM roles [in Amazon's documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html), but it's not necessary in order to follow this setup.

#### Creating a custom IAM role

Go to the [AWS IAM roles dashboard](https://console.aws.amazon.com/iam/home?#/roles) and create a new IAM role for EC2. The role will need to have some specific permissions (see Appendix A), but you can just create a role with the `AmazonEC2RoleforSSM`, `AWSSecurityHubFullAccess` and `AmazonSSMFullAccess` pre-made permissions. In the end it should like something like this:

![Creating a custom IAM role](/images/usage/integrations/monkey-island-aws-screenshot-3.png "Creating a custom IAM role")

#### Applying the IAM role to an instance

For each instance you'd like to access from the island, apply the new IAM role you've just created to the instance. For example:

![Applying a custom IAM role](/images/usage/integrations/monkey-island-aws-screenshot-4.png "Applying a custom IAM role")

After applying the IAM role you should see this screen:

![Applying a custom IAM role](/images/usage/integrations/monkey-island-aws-screenshot-5.png "Applying a custom IAM role")

**Note: after setting IAM roles, the roles might take a few minutes (up to 10 minutes sometimes) to effectively kick in.** This is how AWS works and is not related to the Monkey implementation. See [this StackOverflow thread for more details.](https://stackoverflow.com/questions/20156043/how-long-should-i-wait-after-applying-an-aws-iam-policy-before-it-is-valid)

### Setup SSM agent

If your EC2 instances don't have the _SSM agent_ installed, they will not be able to execute SSM commands, which means you won't see them in the AWS machines table on the monkey island. Generally speaking, most new EC2 instances ought to have SSM pre-installed; The SSM Agent is installed, by default, on Amazon Linux base AMIs dated 2017.09 and later, and on Amazon Linux 2, Ubuntu Server 16.04, and Ubuntu Server 18.04 LTS AMIs.

See [Amazon's documentation about working with SSM agents](https://docs.aws.amazon.com/systems-manager/latest/userguide/ssm-agent.html) for more details on how to check if you have an SSM agent and how to manually  install one if you don't have one.

## Usage

### Running the monkey

When you run the monkey island on an AWS instance, the island detects it's running on AWS and present the following option in the _"Run Monkey"_ page, like so:

![Running a Monkey on EC2 Instance](/images/usage/integrations/monkey-island-aws-screenshot-1.png "Running a Monkey on EC2 Instance")

And then you can choose one of the available instances as "patient zero" like so:

1. Click on "Run on AWS"
2. Choose the relevant Network Interface
3. Select the machines you'd like to run the Monkey on
4. Click "Run on Selected Machines", and watch the monkey go! 🐒

![Running a Monkey on EC2 Instance](/images/usage/integrations/monkey-island-aws-screenshot-2.png "Running a Monkey on EC2 Instance")

## Notes

- The machines which can use IAM roles and be listed MUST be internet connected (or you can set up a proxy for IAM). This is standard AWS practice and you can read about it (and about how to set up the required proxy machines) in AWS IAM documentation.
- You can see the monkey in [the AWS marketplace](https://aws.amazon.com/marketplace/pp/B07B3J7K6D).

### Appendix A: Specific policy permissions required

The IAM role will need to have, at least, the following specific permissions: 

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

#### For exporting security findings to the Security Hub - security hub

_Note: these can be set on the Monkey Island machine alone, since it's the only one exporting findings to the AWS secutiry hub._

- `"securityhub:UpdateFindings"`
- `"securityhub:BatchImportFindings"`

Here's the policy for SecurityHub, as a JSON object:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "securityhub:UpdateFindings",
                "securityhub:BatchImportFindings"
            ],
            "Resource": "*"
        }
    ]
}
```

The JSON object for both of the policies combined therefore is:

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
                "securityhub:UpdateFindings",
                "securityhub:BatchImportFindings",
                "ssm:GetCommandInvocation"
            ],
            "Resource": "*"
        }
    ]
}
```
