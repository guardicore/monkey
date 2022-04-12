CONFIG_URL="https://raw.githubusercontent.com/guardicore/monkey/develop/deployment_scripts/config"

copy_monkey_island_to_build_dir() {
  local src=$1
  local build_dir=$2

  cp "$src"/__init__.py "$build_dir"
  cp "$src"/monkey_island.py "$build_dir"
  cp -r "$src"/common "$build_dir/"

  rsync \
      -ar \
      --exclude=monkey_island/cc/ui/node_modules \
      --exclude=monkey_island/cc/ui/.npm \
      "$src"/monkey_island "$build_dir/"
}

modify_deployment() {
  if [ -n "$1" ]; then
    local deployment_file_path="$2/monkey_island/cc/deployment.json"
    echo -e "{\n    \"deployment\": \"$1\"\n}" > $deployment_file_path
  fi
}

add_agent_binaries_to_build_dir() {
  local agent_binary_dir=$1
  local island_binaries_path="$2/monkey_island/cc/binaries/"

  if [ -z "$agent_binary_dir" ]; then
    download_monkey_agent_binaries $island_binaries_path
  else
    copy_agent_binaries_to_build_dir "$agent_binary_dir" "$island_binaries_path"
  fi

  make_linux_binaries_executable "$island_binaries_path"
}

download_monkey_agent_binaries() {
  local island_binaries_path=$1
  log_message "Downloading monkey agent binaries to ${island_binaries_path}"

  load_monkey_binary_config

  mkdir -p "${island_binaries_path}" || handle_error
  curl -L -o "${island_binaries_path}/${LINUX_64_BINARY_NAME}" "${LINUX_64_BINARY_URL}"
  curl -L -o "${island_binaries_path}/${WINDOWS_64_BINARY_NAME}" "${WINDOWS_64_BINARY_URL}"
}

load_monkey_binary_config() {
  tmpfile=$(mktemp)

  log_message "Downloading prebuilt binary configuration"
  curl -L -s -o "$tmpfile" "$CONFIG_URL"

  log_message "Loading configuration"
  source "$tmpfile"
}

copy_agent_binaries_to_build_dir() {
  cp "$1"/* "$2/"
}

make_linux_binaries_executable() {
  chmod a+x "$1"/monkey-linux-*
}

generate_ssl_cert() {
  local island_path="$1/monkey_island"
  log_message "Generating certificate"

   chmod u+x "$island_path"/linux/create_certificate.sh
  "$island_path"/linux/create_certificate.sh "$island_path"/cc
}

build_frontend() {
  local ui_dir="$1/monkey_island/cc/ui"
  local is_release_build=$2
  pushd "$ui_dir" || handle_error

  log_message "Generating front end"
  npm ci
  if [ "$is_release_build" == true ]; then
    log_message "Running production front end build"
    npm run dist
  else
    log_message "Running development front end build"
    npm run dev
  fi

  popd || handle_error

  remove_node_modules "$ui_dir"
}

remove_node_modules() {
  # Node has served its purpose. We don't need to deliver the node modules with
  # the package.
  rm -rf "$1/node_modules"
  rm -rf "$1/.npm"
}

get_commit_id() {
  local monkey_repo=$1
  echo $(git -C "$monkey_repo" rev-parse --short HEAD)
}
