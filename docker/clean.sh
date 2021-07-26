#!/bin/bash

# This is a utility script to clean up after a failed or successful Docker
# image build in order to speed up development and debugging

BUILD_DIR=$HOME/docker

rm -rf $HOME/git/monkey
rm -rf $BUILD_DIR/monkey
rm -rf $BUILD_DIR/tgz
rm $BUILD_DIR/dk.monkeyisland.*.tar
rm $BUILD_DIR/infection_monkey_docker*.tgz
