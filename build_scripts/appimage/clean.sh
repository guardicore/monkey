#!/bin/bash

# This is a utility script to clean up after a failed or successful AppImage build
# in order to speed up development and debugging.

APPIMAGE_DIR="$(realpath $(dirname $BASH_SOURCE[0]))"

rm -rf "$HOME/git/monkey"
rm -rf "$HOME/.monkey_island"
rm -rf "$APPIMAGE_DIR/squashfs-root"
rm "$APPIMAGE_DIR"/Infection_Monkey*.AppImage
rm "$APPIMAGE_DIR/../dist/InfectionMonkey*.AppImage"
