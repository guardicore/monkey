---
title: "AWS"
date: 2020-05-26T20:57:36+03:00
draft: false
pre: '<i class="fab fa-aws"></i> '
weight: 5
tags: ["setup", "aws"] 
---

## Deployment

On the Infection Monkey’s AWS Marketplace page, click **Continue to Subscribe**.

1. Choose the desired region.
1. Choose an EC2 instance type with at least 1GB of RAM for optimal performance or stick with the recommended.
1. Select the VPC and subnet you want the instance to be in.
1. In the Security Group section, make sure ports 5000 and 5001 on the machine are accessible for inbound TCP traffic.
1. Choose an existing EC2 key pair for authenticating with your new instance.
1. Click **Launch with 1-click.**

At this point, AWS will instance and deploy your new machine.

When ready, you can browse to  the Infection Monkey running on your fresh deployment at:

`https://{public-ip}:5000`

You will be presented a login page. Use the username **monkey**, and the new EC2 instace’s instance ID for password. You can find the instance id by going to the EC2 console and selecting your instance. It should appear in the details pane below.

![AWS instance ID](../../images/setup/aws/aws-instance-id.png "AWS instance ID")
