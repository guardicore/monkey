#!/bin/bash

sources_path=/mnt/sources
build_path=/home/user/Code/chaos_monkey
out_path=/mnt/binaries
out_name=$1
shift
sha=0
update_sha() {
  sha=`ls -lR --time-style=full-iso $sources_path | sha1sum`
}
update_sha
previous_sha=$sha
build() {
  echo -en " building...\n\n"
  rm -fR "$build_path"
  mkdir "$build_path"
  cp -R "$sources_path/." "$build_path"
  pushd "$build_path"
  chmod +x build_linux.sh
  ./build_linux.sh
  popd
  cp -f "$build_path/dist/monkey" "$out_path/$out_name"
  echo -en "\n--> resumed watching."
}
compare() {
  update_sha
  if [[ $sha != $previous_sha ]] ; then
    echo -n "change detected,"
    build
    previous_sha=$sha
  else
    echo -n .
  fi
}
trap build SIGINT
trap exit SIGQUIT

echo -e  "--> Press Ctrl+C to force build, Ctrl+\\ to exit."
echo -en "--> watching \"$path\"."
while true; do
  compare
  sleep 1
done