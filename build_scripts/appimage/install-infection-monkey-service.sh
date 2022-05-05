#!/bin/bash

set -e

SCRIPT_NAME="$(basename "${APPIMAGE}")"
SCRIPT_DIR="$(realpath "$(dirname "${BASH_SOURCE[0]}")")"
SYSTEMD_UNIT_FILENAME="infection-monkey.service"
SYSTEMD_DIR="/lib/systemd/system"
MONKEY_BIN="/opt/infection-monkey/bin"
APPIMAGE_NAME="InfectionMonkey.AppImage"

echo_help() {
  echo "Installs the Infection Monkey service to run on boot."
  echo ""
  echo "Usage:"
  echo "    ${SCRIPT_NAME} service --user <USERNAME>"
  echo "    ${SCRIPT_NAME} service --uninstall"
  echo "    ${SCRIPT_NAME} service -h|--help"
  echo ""
  echo "Options:"
  echo "    --user                      Install Infection Monkey service and run as User"
  echo "    --uninstall                 Uninstall Infection Monkey service"
}

install_service() {
  move_appimage

  cat > "${SCRIPT_DIR}/${SYSTEMD_UNIT_FILENAME}" << EOF
[Unit]
Description=Infection Monkey Runner
After=network.target

[Service]
User=$1
Type=simple
ExecStart="${MONKEY_BIN}/${APPIMAGE_NAME}"

[Install]
WantedBy=multi-user.target
EOF

  umask 077
  sudo mv "${SCRIPT_DIR}/${SYSTEMD_UNIT_FILENAME}" "${SYSTEMD_DIR}/${SYSTEMD_UNIT_FILENAME}"
  sudo systemctl enable "${SYSTEMD_UNIT_FILENAME}" &>/dev/null

  echo -e "The Infection Monkey service has been installed and will start on boot.\n\
Run 'systemctl start infection-monkey' to start the service now."
}

uninstall_service() {
  if [ -f "${MONKEY_BIN}/${APPIMAGE_NAME}" ] ; then
    sudo rm -f "${MONKEY_BIN}/${APPIMAGE_NAME}"
  fi

  if [ -f "${SYSTEMD_DIR}/${SYSTEMD_UNIT_FILENAME}" ] ; then
    sudo systemctl stop "${SYSTEMD_UNIT_FILENAME}" 2>/dev/null
    sudo systemctl disable "${SYSTEMD_UNIT_FILENAME}" &>/dev/null
    sudo rm "${SYSTEMD_DIR}/${SYSTEMD_UNIT_FILENAME}"
    sudo systemctl daemon-reload
  fi

  echo "The Infection Monkey service has been uninstalled"
}

move_appimage() {
  sudo mkdir --mode=0755 -p "${MONKEY_BIN}"

  if [ "${APPIMAGE}" != "${MONKEY_BIN}/${APPIMAGE_NAME}" ] ; then
    umask 022
    sudo cp "${APPIMAGE}" "${MONKEY_BIN}/${APPIMAGE_NAME}"
    sudo chmod 755 "${MONKEY_BIN}/${APPIMAGE_NAME}"
  fi
}

user_exists() {
  id -u "$1" &>/dev/null
}

assert_parameter_supplied() {
  if [ -z "$2" ] ; then
    echo "Error: missing required parameter '$1'"
    echo_help
    exit 1
  fi
}

has_sudo() {
  # 0 true, 1 false
  sudo -nv > /dev/null 2>&1
  return $?
}

exit_if_missing_argument() {
  if [ -z "$2" ] || [ "${2:0:1}" == "-" ]; then
    echo "Error: Argument for parameter '$1' is missing" >&2
    echo_help
    exit 1
  fi
}

do_uninstall=false
username=""

while (( "$#" )); do
  case "$1" in
    --user)
      exit_if_missing_argument "$1" "$2"
      username=$2
      shift 2
      ;;
    --install)
      shift
      ;;
    --uninstall)
      do_uninstall=true
      shift
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

if [ -z "${APPIMAGE}" ] ; then
  echo "Error: Missing 'APPIMAGE' environment variable. Try installing the Infection Monkey service through the AppImage"
  exit 1
fi

if $do_uninstall ; then
  uninstall_service
  exit 0
fi

assert_parameter_supplied "--user" "$username"

if ! user_exists "$username" ; then
  echo "Error: User '$username' does not exist"
  exit 1
fi

install_service "$username"
