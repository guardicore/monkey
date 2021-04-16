#!/bin/bash

# This is a utility script to clean up after a failed or successful AppImage build
# in order to speed up development and debugging.

rm -rf "$HOME/.monkey_island"
rm -rf "$HOME/squashfs-root"
rm -rf "$HOME/git/monkey"
rm "$HOME/appimage/Infection_Monkey-x86_64.AppImage"
