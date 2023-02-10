# Infection Monkey Linux Package Builder

## About

This directory contains the necessary artifacts for building an Infection
Monkey packages for Linux.

## AppImage

### Building an AppImage

1. Create a clean VM or LXD (not docker!) based on Ubuntu 18.04.
1. Copy the `build_scipts/` directory to `$HOME/` in the VM.
1. On the VM, `cd $HOME/build_scripts`
1. Run `sudo -v`.
1. Execute `./build_appimage.sh`. This will pull all necessary dependencies
   and build the AppImage.

NOTE: This script is intended to be run from a clean VM. You can also manually
remove build artifacts by running `appimage/clean.sh`

WARNING: If you use a LXD container, ensure that shiftfs is disabled.

### Running the AppImage

The build script will produce an AppImage executable named
`./dist/Infection_Monkey-x86_64.AppImage`. Simply execute this file and you're off to
the races.

A new directory, `$HOME/.monkey_island` will be created to store runtime
artifacts.

## Docker

### Building a Docker image
1. Create a clean Ubuntu 18.04 VM (not WSL).
1. Copy the `build_scipts/` directory to `$HOME/` in the VM.
1. On the VM, `cd $HOME/build_scripts`
1. Run `sudo -v`.
1. Execute `./build_docker.sh --package docker`. This will pull all necessary dependencies
   and build the Docker image.

NOTE: This script is intended to be run from a clean VM. You can also manually
remove build artifacts by running `docker/clean.sh`

### Running the Docker Image
The build script will produce a `.tgz` file in `./dist/`. See
`docker/DOCKER_README.md` for instructions on running the docker image.
