#!/bin/bash

exists() {
  command -v "$1" >/dev/null 2>&1
}

export os_version_monkey=$(cat /etc/issue)
MONGODB_DIR=$1 # If using deb, this should be: /var/monkey/monkey_island/bin/mongodb

if [[ ${os_version_monkey} == "Ubuntu 16.04"* ]]; then
  echo Detected Ubuntu 16.04
  export tgz_url="https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1604-3.6.12.tgz"
elif [[ ${os_version_monkey} == "Ubuntu 18.04"* ]]; then
  echo Detected Ubuntu 18.04
  export tgz_url="https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1804-4.2.0.tgz"
elif [[ ${os_version_monkey} == "Debian GNU/Linux 8"* ]]; then
  echo Detected Debian 8
  export tgz_url="https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-debian81-3.6.12.tgz"
elif [[ ${os_version_monkey} == "Debian GNU/Linux 9"* ]]; then
  echo Detected Debian 9
  export tgz_url="https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-debian92-3.6.12.tgz"
else
  echo Unsupported OS
  exit 1
fi

TEMP_MONGO=$(mktemp -d)
pushd "${TEMP_MONGO}"

if exists bash; then
  wget ${tgz_url} -O mongodb.tgz
else
  if exists curl; then
    curl --output mongodb.tgz ${tgz_url}
  else
    echo 'Your system has neither curl nor wget, exiting'
    exit 1
  fi
fi

tar -xf mongodb.tgz
popd

mkdir -p "${MONGODB_DIR}"/bin
mkdir -p "${MONGODB_DIR}"/db
cp "${TEMP_MONGO}"/mongodb-*/bin/mongod "${MONGODB_DIR}"/bin/mongod
cp "${TEMP_MONGO}"/mongodb-*/LICENSE-Community.txt "${MONGODB_DIR}"/
chmod a+x "${MONGODB_DIR}"/bin/mongod
# shellcheck disable=SC2086
rm -r ${TEMP_MONGO}

exit 0
