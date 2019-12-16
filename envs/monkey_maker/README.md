# Monkey maker

## About

Monkey maker is an environment on AWS that 
is designed for monkey binary building. 
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

