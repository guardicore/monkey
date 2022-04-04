#!/bin/bash

set -e

SCRIPT_DIR="$(realpath $(dirname $BASH_SOURCE[0]))"
SYSTEMD_UNIT_FILENAME="monkey-appimage.service"
SYSTEMD_DIR="/lib/systemd/system"
MONKEY_BIN="/opt/infection-monkey/bin"
APPIMAGE_NAME="InfectionMonkey.appimage"

echo_help() {
  echo "usage: install-infection-monkey-service.sh [--user <NAME> --appimage <PATH>] [--help] [--uninstall]"
  echo ""
  echo "Installs Infection Monkey AppImage and systemd unit to run on boot"
  echo "--user                          User to run the AppImage as"
  echo "--appimage                      Path to the AppImage"
  echo "--uninstall                     Uninstall Infection Monkey AppImage systemd service"
}

service_install() {
  cat > "${SCRIPT_DIR}/${SYSTEMD_UNIT_FILENAME}" << EOF
[Unit]
Description=Infection Monkey AppImage Runner
After=network.target

[Service]
User=$1
Type=simple
ExecStart="${MONKEY_BIN}/${APPIMAGE_NAME}"

[Install]
WantedBy=multi-user.target
EOF

  sudo mv "${SCRIPT_DIR}/${SYSTEMD_UNIT_FILENAME}" "${SYSTEMD_DIR}/${SYSTEMD_UNIT_FILENAME}"

  # Enable on boot
  sudo systemctl enable "${SYSTEMD_UNIT_FILENAME}" &>/dev/null
  sudo systemctl daemon-reload
}

service_uninstall() {
  echo "Uninstalling Infection Monkey AppImage systemd service..."

  if [ -f "${MONKEY_BIN}/${APPIMAGE_NAME}" ] ; then
    sudo rm -f "${MONKEY_BIN}/${APPIMAGE_NAME}"
  fi

  if [ -f "${SYSTEMD_DIR}/${SYSTEMD_UNIT_FILENAME}" ] ; then
    sudo systemctl stop "${SYSTEMD_UNIT_FILENAME}" 2>/dev/null
    sudo systemctl disable "${SYSTEMD_UNIT_FILENAME}" &>/dev/null
    sudo rm "${SYSTEMD_DIR}/${SYSTEMD_UNIT_FILENAME}"
    sudo systemctl daemon-reload
  fi

  exit 0
}

has_sudo() {
  # 0 true, 1 false
  sudo -nv > /dev/null 2>&1
  return $?
}

exit_if_missing_argument() {
  if [ -z "$2" ] || [ "${2:0:1}" == "-" ]; then
    echo "Error: Argument for $1 is missing" >&2
    exit 1
  fi
}

uname=""
appimage_path=""

while (( "$#" )); do
  case "$1" in
    --user)
      exit_if_missing_argument "$1" "$2"

      uname=$2
      shift 2
      ;;
    --appimage)
      exit_if_missing_argument "$1" "$2"

      appimage_path=$2
      shift 2
      ;;
    --uninstall)
      service_uninstall
      ;;
    -h|--help)
      echo_help
      exit 0
      ;;
    *)
      echo "Error: Unsupported parameter $1" >&2
      exit 1
      ;;
  esac
done

if ! has_sudo; then
  echo "Error: You need root permissions for some of this script operations. \
Run \`sudo -v\`, enter your password, and then re-run this script."
  exit 1
fi

# input sanity
if [ -z "$uname" ] || [ -z "$appimage_path" ] ; then
  echo "Error: missing flags"
  echo_help
  exit 1
fi

# specified user exists
if ! id -u "$uname" &>/dev/null ; then
  echo "Error: User does not exist '${uname}'"
  exit 1
fi

# appimage path exists
if [ ! -f "${appimage_path}" ] ; then
  if [ ! -f "${SCRIPT_DIR}/${appimage_path}" ] ; then
    echo "Error: AppImage path does not exist: '${appimage_path}'"
    exit 1
  fi
  appimage_path="${SCRIPT_DIR}/${appimage_path}"
fi

# move appimge to dst dir
sudo mkdir -p "${MONKEY_BIN}"
if [ "$appimage_path" != "${MONKEY_BIN}/${APPIMAGE_NAME}" ] ; then
  sudo cp "$appimage_path" "${MONKEY_BIN}/${APPIMAGE_NAME}"
fi

service_install "${uname}"
echo "Installation done. "
