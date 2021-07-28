# Infection Monkey

How to run Monkey Island from the docker file:

Note: Ports 5000 and 5001 must be available for the island to work.

## Setup

Run the following commands:

```sh
sudo docker load -i dk.monkeyisland.MONKEY_VER_PLACEHOLDER.tar
sudo docker pull mongo:4.2
sudo mkdir -p /var/monkey-mongo/data/db
sudo docker run --name monkey-mongo --network=host -v /var/monkey-mongo/data/db:/data/db -d mongo:4.2
sudo docker run --name monkey-island --network=host -d guardicore/monkey-island:MONKEY_VER_PLACEHOLDER
```

## Start Infecting

Open `https://<Server IP>:5000` using Google Chrome and follow the instructions. You can also visit [the Infection Monkey website](https://infectionmonkey.com) and read the in-depth Getting Started guides.
