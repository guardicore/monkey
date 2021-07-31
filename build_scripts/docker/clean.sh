#!/bin/bash

# This is a utility script to clean up after a failed or successful Docker
# image build in order to speed up development and debugging

DOCKER_DIR="$(realpath $(dirname $BASH_SOURCE[0]))"


rm -rf "$HOME/git/monkey"
rm -rf "$DOCKER_DIR/monkey"
rm -rf "$DOCKER_DIR/tgz"
rm "$DOCKER_DIR"/dk.monkeyisland.*.tar
rm "$DOCKER_DIR"/infection_monkey_docker*.tgz
rm "$DOCKER_DIR"/../dist/infection_monkey_docker*.tgz
