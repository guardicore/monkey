#!/bin/bash

set -e

SCRIPT_DIR="$(realpath "$(dirname "${BASH_SOURCE[0]}")")"
SYSTEMD_UNIT_FILENAME="infection-monkey.service"
SYSTEMD_DIR="/lib/systemd/system"
MONKEY_BIN="/opt/infection-monkey/bin"
APPIMAGE_NAME="InfectionMonkey.appimage"

echo_help() {
  echo "Installs Infection Monkey service to run on boot"
  echo ""
  echo "Usage:"
  echo "    install-infection-monkey-service.sh --user <NAME> --appimage <PATH>"
  echo "    install-infection-monkey-service.sh --uninstall"
  echo "    install-infection-monkey-service.sh -h|--help"
  echo ""
  echo "Options:"
  echo "    --user                      User to run the service as"
  echo "    --appimage               	Path to AppImage"
  echo "    --uninstall                 Uninstall Infection Monkey service"
}

install_service() {
  move_appimage "$2"

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
  sudo mkdir -p "${MONKEY_BIN}"

  if [ "$1" != "${MONKEY_BIN}/${APPIMAGE_NAME}" ] ; then
    sudo cp "$appimage_path" "${MONKEY_BIN}/${APPIMAGE_NAME}"
  fi

  sudo chmod a+x "${MONKEY_BIN}/${APPIMAGE_NAME}"
}

user_exists() {
  id -u "$1" &>/dev/null
}

assert_parameter_supplied() {
  if [ -z "$2" ] ; then
    echo "Error: missing flag '$1'"
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
    echo "Error: Argument for $1 is missing" >&2
    exit 1
  fi
}

do_uninstall=false
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

if $do_uninstall ; then
  uninstall_service
  exit 0
fi

assert_parameter_supplied "--user" "$uname"
assert_parameter_supplied "--appimage" "$appimage_path"

if ! user_exists "$uname" ; then
  echo "Error: User '$uname' does not exist"
  exit 1
fi

if [ ! -f "$appimage_path" ] ; then
  if [ ! -f "${SCRIPT_DIR}/$appimage_path" ] ; then
    echo "Error: AppImage '$appimage_path' does not exist"
    exit 1
  fi
  appimage_path="${SCRIPT_DIR}/$appimage_path"
fi

install_service "$uname" "$appimage_path"

