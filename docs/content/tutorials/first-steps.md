---
title: "Tutorial 0: First steps"
date: 2020-05-26T20:57:10+03:00
draft: false
pre: '<i class="fas fa-shoe-prints"></i> '
weight: 2
tags: ["tutorials", "first-steps"]
---

In this tutorial, we will setup a simple sandbox environment that will be
useful in future tutorials. We will learn how to access the Infection Monkey's
command and control server and register a new user.

### Prerequisites
First, make sure that you have the following installed:
- `docker` and `docker-compose`

### Run the environment
Next, we'll use `docker compose` to run Infection Monkey along with our
vulnerable container.

1. Download the following compose file:
   [docker-compose.yml](docker/docker-compose.yaml)

2. Then, navigate to the directory where you downloaded the file and run the
   following command to start the environment:

   ```
   docker compose up
   ```

Now you should have 3 containers running:
- `monkey-island` - the Infection Monkey server
- `mongo` - database used by Infection Monkey
- `hello` - a vulnerable container

You can confirm this by running
```
$ docker container ls --format "table {{.ID}}\t{{.Names}}\t{{.Status}}"
CONTAINER ID   NAMES           STATUS
737b67cc344c   monkey-island   Up 7 seconds
fbd91aacc8ea   mongo           Up 7 seconds
b1c9ac1d3b81   hello           Up 7 seconds
```

Now that the environment is running, open a browser to
[https://localhost:5000](https://localhost:5000) to access the Monkey Island
web interface. You may see a warning that looks similar to the one shown below.
For this tutorial, you can safely ignore this warning by clicking _Advanced_
followed by _Proceed to localhost (unsafe)_. ![Self-signed certificate
warning](../../images/tutorials/first-steps/010-certificate.jpg)

Since this is the first time you're accessing this Infection
Monkey instance, you'll need to register. Provide a username and password, and
then click _Let's go!_.

![Infection Monkey login
screen](../../images/tutorials/first-steps/020-registration-page.jpg)

After registering, you'll be automatically logged in and taken to the **Getting
Started** page.

![Getting started
page](../../images/tutorials/first-steps/030-getting-started-page.jpg)
🎉 Congratulations 🎉 Your environment is up and running!

### Review
Let's take a moment to review what you've learned:
- You now know how to create a sandbox environment for experimenting with
  Infection Monkey using Docker.
- You've learned how register a user with Infection Monkey.


### Next steps
Now that you have a sandbox environment for experimenting with Infection
Monkey, you can move on to [Tutorial 1: Hello, Monkey](../hello-monkey), where
you'll learn how to configure and use Infection Monkey to exploit a vulnerable
server.

If you'd like to install Infection Monkey on a different platform, you can find
instructions on the [Setup](../../setup) page.
