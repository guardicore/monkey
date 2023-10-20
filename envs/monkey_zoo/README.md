# MonkeyZoo
These files are used to deploy Infection Monkey's test network on GCP.<br>

## Warning\!

This project builds an intentionally
<span class="underline">vulnerable</span> network. Make sure not to add
production servers to the same network and leave it closed to the
public.

## Introduction:

MonkeyZoo is a Google Cloud Platform network deployed with terraform.
Terraform scripts allows you to quickly setup a network that’s full of
vulnerable machines to regression test monkey’s exploiters, evaluate
scanning times in a real-world scenario and many more.

## Building MonkeyZoo Images

### Requirements
- [Packer](https://developer.hashicorp.com/packer/downloads)
- [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#installing-ansible)
- An S3 bucket for storing terraform state
- A [GCP Service Account](https://developers.google.com/identity/protocols/oauth2/service-account#creatinganaccount) for the project in which to create the images
  - This account should have `Service Account User` and `Compute Instance Admin` permissions
- A GCP key file for the service account

The following commands assume that packer is run from the envs/monkey_zoo/packer directory.

To install the requirements run `packer init`, e.g.:
```bash
packer init .
```

Make sure that the values in `variables.pkr.hcl` and `variables.auto.pkrvars.hcl` are correct for your environment.
Then, run the `packer build` to build the images for the MonkeyZoo. These are the images from which the zoo will be deployed.

Example:
  `packer build .`

Example:
  `packer build -only googlecompute.mimikatz-15,googlecompute.snmp-20 .`

If you want to disable parallelization and output debugging info, add `-debug` flag to the command.
If you want to allow editing and retrying of a failed script, use the `-on-error=ask` flag.
If you want to override an already existing image add `-force` flag to the command.

## MonkeyZoo network

Check [MonkeyZoo network](docs/zoo_network.md) documentation on how machines are setup
and how the network of the vulnerable machines looks.

## Setting up a MonkeyZoo

To set up and use a MonkeyZoo network on GCP using terraform refer to [MonkeyZoo setup](docs/zoo_setup.md).

## Running manual tests

MonkeyZoo test network can be used to test the majority of Infection Monkey features.

### Exploiting machines

Most of the machines in [network documentation](docs/zoo_network.md) can be exploited with a
corresponding exploiter. Navigate to a machine you'd like to exploit and add its IP to the target
list in the configuration. If it's a brute-force exploiter, you'll also need to add the password/credentials
shown in the table (if a username is not present it's usually `m0nk3y`).

### Testing other features

Zoo is also used to test other features, like multi-hop exploitation or credential stealing.

Some diagrams for more complex exploitation network topography tests can be found in `envs/monkey_zoo/docs/network_diagrams`.
If you want to exercise these make sure to configure more hops/exploitation depth in the configuration.

Lastly, feel free to use the Zoo network to configure and test other features. Read through the descriptions
in the [network documentation](docs/zoo_network.md) and if you can't find a machine to satisfy your test case,
refer to our [usage documentation](https://techdocs.akamai.com/infection-monkey/docs/usage).

If you run into trouble talk to us on our [Slack channel](https://infectionmonkey.slack.com/join/shared_invite/enQtNDU5MjAxMjg1MjU1LWM0NjVmNWE2ZTMzYzAxOWJiYmMxMzU0NWU3NmUxYjcyNjk0YWY2MDkwODk4NGMyNDU4NzA4MDljOWNmZWViNDU),
email us at support@infectionmonkey.com or open an issue on [GitHub](https://github.com/guardicore/monkey).

## Running blackbox tests

To run blackbox tests on the newly created MonkeyZoo network refer to [Blackbox test dcoumentation](blackbox/README.md).
