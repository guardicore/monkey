# Monkey Island Docker Image

## About

This directory contains the necessary artifacts for building an Infection
Monkey Docker image.

## Building a Docker image
1. Create a clean Ubuntu 18.04 VM (not WSL).
1. Copy the `docker/` directory to `$HOME/` in the VM.
1. On the VM, `cd $HOME/docker`
1. Run `sudo -v`.
1. Execute `./build_docker.sh`. This will pull all necessary dependencies
   and build the Docker image.

NOTE: This script is intended to be run from a clean VM. You can also manually
remove build rtifacts by running `docker/clean.sh`

## Running the Docker Image
See `docker/DOCKER_README.md` for instructions on running the docker image.
