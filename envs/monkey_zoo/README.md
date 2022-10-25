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

## MonkeyZoo network

Check [MonkeyZoo network](docs/zoo_network.md) documentation on how machines are setup
and how the network of the vulnerable machines looks.

## Setting up a MonkeyZoo

To set up and use a MonkeyZoo network on GCP using terraform refer to [MonkeyZoo setup](docs/zoo_setup.md).

## Running blackbox tests

To run blackbox tests on the newly created MonkeyZoo network refer to [Blackbox test dcoumentation](blackbox/README.md).
