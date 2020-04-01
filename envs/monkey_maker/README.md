# Monkey maker

## About

Monkey maker is an environment on AWS that 
is designed for monkey binary building. 
This environment is deployed using terraform scripts
located in this directory.

## Setup

To setup you need to put `accessKeys` file into `./aws_keys` directory.

Contents of `accessKeys` file should be as follows:

```ini
[default]
aws_access_key_id = <...>
aws_secret_access_key = <...>
```
Also review `./terraform/config.tf` file.

Launch the environment by going into `terraform` folder and running
```
terraform init
terraform apply
```

## Usage

To login to windows use Administrator: %HwuzI!Uzsyfa=cB*XaQ6xxHqopfj)h) credentials

You'll find docker files in `/home/ubuntu/docker_envs/linux/...`

To build docker image for 32 bit linux: 
```
cd /home/ubuntu/docker_envs/linux/py3-32
sudo docker build -t builder32 .
```

To build docker image for 64 bit linux: 
```
cd /home/ubuntu/docker_envs/linux/py3-64
sudo docker build -t builder64 .
```

To build 32 bit monkey binary:
```
cd /home/ubuntu/monkey_folder/monkey
sudo docker run -v "$(pwd):/src" builder32 -c "export SRCDIR=/src/infection_monkey && /entrypoint.sh"
```

To build 64 bit monkey binary:
```
cd /home/ubuntu/monkey_folder/monkey
sudo docker run -v "$(pwd):/src" builder64 -c "export SRCDIR=/src/infection_monkey && /entrypoint.sh"
```
