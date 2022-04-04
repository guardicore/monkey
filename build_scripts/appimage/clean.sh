#!/bin/bash

# This is a utility script to clean up after a failed or successful AppImage build
# in order to speed up development and debugging.

APPIMAGE_DIR="$(realpath $(dirname $BASH_SOURCE[0]))"
SYSTEMD_UNIT_FILENAME="monkey.service"
SYSTEMD_DIR="/lib/systemd/system"

rm -rf "$HOME/git/monkey"
rm -rf "$HOME/.monkey_island"
rm -rf "$APPIMAGE_DIR/squashfs-root"
rm "$APPIMAGE_DIR"/Infection_Monkey*.AppImage
rm "$APPIMAGE_DIR/../dist/InfectionMonkey*.AppImage"

if [ -f "${SYSTEMD_DIR}/${SYSTEMD_UNIT_FILENAME}" ] ; then
  sudo systemctl stop "${SYSTEMD_UNIT_FILENAME}" 2>/dev/null
  sudo systemctl disable "${SYSTEMD_UNIT_FILENAME}"
  sudo rm "${SYSTEMD_DIR}/${SYSTEMD_UNIT_FILENAME}"
  sudo systemctl daemon-reload
fi
