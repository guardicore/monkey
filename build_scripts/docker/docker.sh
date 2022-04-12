DOCKER_DIR="$(realpath $(dirname $BASH_SOURCE[0]))"

source "$DOCKER_DIR/../common.sh"

install_package_specific_build_prereqs() {
    sudo apt-get install -y docker.io
}

setup_build_dir() {
  local agent_binary_dir=$1
  local monkey_repo=$2
  local is_release_build=$4
  local build_dir=$DOCKER_DIR/monkey

  mkdir "$build_dir"

  copy_entrypoint_to_build_dir "$build_dir"

  copy_monkey_island_to_build_dir "$monkey_repo/monkey" "$build_dir"
  copy_server_config_to_build_dir "$build_dir"
  modify_deployment "$deployment_type" "$build_dir"
  add_agent_binaries_to_build_dir "$agent_binary_dir" "$build_dir"

  generate_ssl_cert "$build_dir"

  build_frontend "$build_dir" "$is_release_build"
}

copy_entrypoint_to_build_dir() {
  cp "$DOCKER_DIR"/entrypoint.sh "$1"
  chmod 755 "$1/entrypoint.sh"
}

copy_server_config_to_build_dir() {
  cp "$DOCKER_DIR"/server_config.json "$1"/monkey_island/cc
}

build_package() {
  local version=$1
  local commit_id=$2
  local dist_dir=$3
  pushd ./docker

  if [ -n "$1" ]; then
    version="v$version"
  else
    version="$commit_id"
  fi

  docker_image_name="guardicore/monkey-island:$version"
  tar_name="$DOCKER_DIR/InfectionMonkey-docker-$version.tar"

  build_docker_image_tar "$docker_image_name" "$tar_name"

  tgz_name="$DOCKER_DIR/InfectionMonkey-docker-$version.tgz"
  build_docker_image_tgz "$tar_name" "$tgz_name"

  move_package_to_dist_dir $tgz_name $dist_dir

  popd
}

build_docker_image_tar() {
  sudo docker build . -t "$1"
  sudo docker save "$1" > "$2"
}

build_docker_image_tgz() {
  mkdir tgz
  mv "$1" ./tgz
  cp ./DOCKER_README.md ./tgz/README.md
  tar -C ./tgz -cvf "$2" --gzip .
}

move_package_to_dist_dir() {
    mv "$1" "$2/"
}
