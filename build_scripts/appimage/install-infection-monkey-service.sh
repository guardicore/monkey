#!/bin/bash

set -e

SCRIPT_NAME="$(basename "${APPIMAGE}")"
SYSTEMD_UNIT_FILENAME="infection-monkey.service"
TMP_SYSTEMD_UNIT="${PWD}/${SYSTEMD_UNIT_FILENAME}"
SYSTEMD_DIR="/lib/systemd/system"
MONKEY_BIN="/opt/infection-monkey/bin"
APPIMAGE_NAME="InfectionMonkey.AppImage"
MONKEY_DATA_DIR="$HOME/.monkey_island"

die() {
    echo "$1" >&2
    echo ""
    echo_help
    exit 1
}

echo_help() {
  echo "Installs the Infection Monkey service to run on boot."
  echo ""
  echo "Usage:"
  echo "    ${SCRIPT_NAME} service --install --user <USERNAME>"
  echo "    ${SCRIPT_NAME} service --uninstall"
  echo "    ${SCRIPT_NAME} service -h|--help"
  echo ""
  echo "Options:"
  echo "    --install                   Install the Infection Monkey service"
  echo "    --user                      Configure the Infection Monkey service to run as a specific user"
  echo "    --uninstall                 Uninstall Infection Monkey service"
}

install_service() {
  exit_if_service_installed
  copy_appimage
  install_systemd_unit "$1"

  echo "The Infection Monkey service has been installed and will start on boot."
  echo "Run 'systemctl start infection-monkey' to start the service now."
}

exit_if_service_installed() {
  if sudo systemctl list-units --full --all | grep -Fq "${SYSTEMD_UNIT_FILENAME}"; then
    echo "Error: Service ${SYSTEMD_UNIT_FILENAME} is already installed."
    echo -e "Please uninstall it with \033[1msudo ${SCRIPT_NAME} service --uninstall\033[0m before proceeding."
    die
  fi
}

copy_appimage() {
  sudo mkdir --mode=0755 -p "${MONKEY_BIN}"

  if [ "${APPIMAGE}" != "${MONKEY_BIN}/${APPIMAGE_NAME}" ] ; then
    umask 022
    sudo cp "${APPIMAGE}" "${MONKEY_BIN}/${APPIMAGE_NAME}"
    sudo chmod 755 "${MONKEY_BIN}/${APPIMAGE_NAME}"
  fi
}

install_systemd_unit() {
  umask 077
  cat > "${TMP_SYSTEMD_UNIT}" << EOF
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

  sudo mv "${TMP_SYSTEMD_UNIT}" "${SYSTEMD_DIR}/${SYSTEMD_UNIT_FILENAME}"
  sudo systemctl enable "${SYSTEMD_UNIT_FILENAME}" &>/dev/null
}

uninstall_service() {
  if [ -d "${MONKEY_DATA_DIR}" ] ; then
    read -r -p "Existing data directory (${MONKEY_DATA_DIR}) needs to be deleted. All data from previous runs will be lost. Proceed to delete? (y/n) " choice

    case "$choice" in
      y|Y )
        username=$(systemctl show -p User ${SYSTEMD_UNIT_FILENAME} | cut -d'=' -f2)
        sudo -u "${username}" rm -rf "${MONKEY_DATA_DIR}"
        ;;
      n|N )
        die "Unable to uninstall ${SYSTEMD_UNIT_FILENAME}. Please backup and delete the existing data directory (${MONKEY_DATA_DIR}). Then, try again. To learn how to restore and use a backup, please refer to the documentation."
        ;;
      * )
        die "Invalid input. Please enter 'y' or 'n'."
        ;;
    esac
  fi

  if [ -f "${MONKEY_BIN}/${APPIMAGE_NAME}" ] ; then
    sudo rm -f "${MONKEY_BIN}/${APPIMAGE_NAME}"
  fi

  if [ -f "${SYSTEMD_DIR}/${SYSTEMD_UNIT_FILENAME}" ] ; then
    sudo systemctl stop "${SYSTEMD_UNIT_FILENAME}" 2>/dev/null
    sudo systemctl disable "${SYSTEMD_UNIT_FILENAME}" &>/dev/null
    sudo rm "${SYSTEMD_DIR}/${SYSTEMD_UNIT_FILENAME}"
    sudo systemctl daemon-reload
  fi

  echo "The Infection Monkey service has been uninstalled. Data directory ${MONKEY_DATA_DIR} has been removed."
}

exit_if_user_doesnt_exist() {
    if ! user_exists "$1" ; then
      die "Error: User '$1' does not exist."
    fi
}

user_exists() {
  id -u "$1" &>/dev/null
}

has_sudo() {
  # 0 true, 1 false
  sudo -nv > /dev/null 2>&1
  return $?
}

exit_if_missing_argument() {
  if [ -z "$2" ] || [ "${2:0:1}" == "-" ]; then
    die "Error: Argument for parameter '$1' is missing."
  fi
}

do_uninstall=false
do_install=false
username=""

while (( "$#" )); do
  case "$1" in
    --user)
      exit_if_missing_argument "$1" "$2"
      exit_if_user_doesnt_exist "$2"
      username=$2
      shift 2
      ;;
    --install)
      do_install=true
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
      die "Error: Unsupported parameter \"$1\"."
      ;;
  esac
done

if ! has_sudo; then
  die "Error: You need root permissions for some of this script operations. \
Run \`sudo -v\`, enter your password, and then re-run this script."
fi

if [ -z "${APPIMAGE}" ] ; then
  die "Error: Missing 'APPIMAGE' environment variable. Try installing the Infection Monkey service through the AppImage"
fi

if $do_install && $do_uninstall ; then
    die "Error: The --install and --uninstall flags are mutually exclusive."
fi

if $do_uninstall ; then
  uninstall_service "$username"
  exit 0
fi

if $do_install ; then
    if [ -z "$username" ] ; then
        die "Error: You must supply a username."
    fi

    install_service "$username"
    exit 0
fi

die "Error:You must specify either the --install or --uninstall flag."
