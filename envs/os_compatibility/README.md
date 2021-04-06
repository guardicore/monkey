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

0. Add your machine's IP to the `os_compat_island` security group ingress rules.
1. Launch os_compat_ISLAND machine and upload your binaries/update island. Reset island environment.
2. Launch/Reboot all other os_compat test machines (Can be filtered with tag "Purpose: os_compat_instance")
3. Wait until machines boot and run monkey
4. Launch `test_compatibility.py` pytest script with island ip parameter 
(e.g. `test_compatibility.py --island 111.111.111.111:5000`)

## Machines

Since island machine is built from custom AMI it already has the following credentials:

Administrator: %tPHGz8ZuQsBnEUgdpz!6f&elGnFy?;.

For windows_2008_r2 Administrator:AGE(MP..txL

The following machines does not download monkey automatically, so you'll have to manually check them:

- os_compat_kali_2019
- os_compat_oracle_6
- os_compat_oracle_7
- windows_2003_r2_32
- windows_2003
- windows_2008_r2

A quick reference for usernames on different machines (if in doubt check official docs):
- Ubuntu: ubuntu
- Oracle: clckwrk
- CentOS: centos
- Debian: admin
- Everything else: ec2-user

To manually verify the machine is compatible use commands to download and execute the monkey.
Also, add your IP to `os_compat_instance` security group.

Example commands:
 - Powershell:
```cmd
[System.Net.ServicePointManager]::CertificatePolicy = New-Object TrustAllCertsPolicy
Set-MpPreference -DisableRealtimeMonitoring $true -ErrorAction SilentlyContinue
Invoke-WebRequest -Uri 'https://10.0.0.251:5000/api/monkey/download/monkey-windows-64.exe' -OutFile 'C:\windows\temp\monkey-windows-64.exe' -UseBasicParsing
C:\windows\temp\monkey-windows-64.exe m0nk3y -s 10.0.0.251:5000
```

 - Bash:
```shell script
wget --no-check-certificate -q https://10.0.0.251:5000/api/monkey/download/monkey-linux-64 -O ./monkey-linux-64 || curl https://10.0.0.251:5000/api/monkey/download/monkey-linux-64 -k -o monkey-linux-64
chmod +x ./monkey-linux-64
./monkey-linux-64 m0nk3y -s 10.0.0.251:5000
```
