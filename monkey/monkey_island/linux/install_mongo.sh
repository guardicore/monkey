#!/bin/bash

exists() {
  command -v "$1" >/dev/null 2>&1
}

os_version_monkey=$(cat /etc/issue)
export os_version_monkey
MONGODB_DIR=$1 # If using deb, this should be: /var/monkey/monkey_island/bin/mongodb

if [[ ${os_version_monkey} == "Ubuntu 18.04"* ]]; then
  echo Detected Ubuntu 18.04
  export tgz_url="https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1804-6.0.4.tgz"
elif [[ ${os_version_monkey} == "Ubuntu 20.04"* ]]; then
  echo Detected Ubuntu 20.04
  export tgz_url="https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu2004-6.0.4.tgz"
elif [[ ${os_version_monkey} == "Ubuntu 22.04"* ]]; then
  echo Detected Ubuntu 22.04
  export tgz_url="https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu2204-6.0.4.tgz"
elif [[ ${os_version_monkey} == "Debian GNU/Linux 10"* ]]; then
  echo Detected Debian 10
  export tgz_url="https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-debian10-6.0.4.tgz"
elif [[ ${os_version_monkey} == "Debian GNU/Linux 11"* ]]; then
  echo Detected Debian 11
  export tgz_url="https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-debian11-6.0.4.tgz"
elif [[ ${os_version_monkey} == "Kali GNU/Linux"* ]]; then
  echo Detected Kali Linux
  export tgz_url="https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-debian10-6.0.4.tgz"
else
  echo Unsupported OS
  exit 1
fi

TEMP_MONGO=$(mktemp -d)
pushd "${TEMP_MONGO}" || {
  echo "Pushd failed"
  exit 1
}

if exists wget; then
  wget -q ${tgz_url} -O mongodb.tgz
else
  if exists curl; then
    curl --output mongodb.tgz ${tgz_url}
  else
    echo 'Your system has neither curl nor wget, exiting'
    exit 1
  fi
fi

tar -xf mongodb.tgz
popd || {
  echo "popd failed"
  exit 1
}

mkdir -p "${MONGODB_DIR}"/bin
cp "${TEMP_MONGO}"/mongodb-*/bin/mongod "${MONGODB_DIR}"/bin/mongod
cp "${TEMP_MONGO}"/mongodb-*/LICENSE-Community.txt "${MONGODB_DIR}"/
chmod a+x "${MONGODB_DIR}"/bin/mongod
rm -r "${TEMP_MONGO}"

exit 0
