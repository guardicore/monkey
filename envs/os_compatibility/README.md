# OS compatibility

## About

OS compatibility is an environment on AWS that 
is designed to test monkey binary compatibility on
different operating systems. 
This environment is deployed using terraform scripts
located in this directory.

## Setup

To setup you need to put `accessKeys` file into `./aws_keys` directory.

Contents of `accessKeys` file should be as follows:

```
[default]
aws_access_key_id = <...>
aws_secret_access_key = <...>
```
Also review `./terraform/config.tf` file.

Launch the environment by going into `terraform` folder and running
```angular2html
terraform init
terraform apply
```

## Usage

1. Launch os_compat_ISLAND machine and upload your binaries/update island. Reset island environment.
2. Launch/Reboot all other os_compat test machines (Can be filtered with tag "Puropose: os_compat_instance")
3. Wait until machines boot and run monkey
4. Launch `test_compatibility.py` pytest script with island ip parameter 
(e.g. `test_compatibility.py --island 111.111.111.111:5000`)

## Machines

Since island machine is built from custom AMI it already has the following credentials:

Administrator: %tPHGz8ZuQsBnEUgdpz!6f&elGnFy?;.

The following machines does not download monkey automatically, so you'll have to manually check them:

- os_compat_kali_2019
- os_compat_oracle_6
- os_compat_oracle_7
- windows_2003_r2_32
- windows_2003

A quick reference for usernames on different machines (if in doubt check official docs):
- Ubuntu: ubuntu
- Oracle: clckwrk
- CentOS: centos
- Everything else: ec2-user

