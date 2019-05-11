#!/bin/bash

export os_version_monkey=$(cat /etc/issue)
MONGODB_DIR=$1 # If using deb, this should be: /var/monkey/monkey_island/bin/mongodb

if [[ ${os_version_monkey} == "Ubuntu 16.04"* ]] ;
then
	echo Detected Ubuntu 16.04
	export tgz_url="https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1604-3.6.12.tgz"
elif [[ ${os_version_monkey} == "Ubuntu 18.04"* ]] ;
then
	echo Detected Ubuntu 18.04
	export tgz_url="https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1804-4.0.8.tgz"
elif [[ ${os_version_monkey} == "Debian GNU/Linux 8"* ]] ;
then
	echo Detected Debian 8
	export tgz_url="https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-debian81-3.6.12.tgz"
elif [[ ${os_version_monkey} == "Debian GNU/Linux 9"* ]] ;
then
	echo Detected Debian 9
	export tgz_url="https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-debian92-3.6.12.tgz"
else
	echo Unsupported OS
	exit -1
fi

TEMP_MONGO=$(mktemp -d)
pushd ${TEMP_MONGO}
wget ${tgz_url} -O mongodb.tgz
tar -xf mongodb.tgz
popd

mkdir -p ${MONGODB_DIR}/bin
cp ${TEMP_MONGO}/mongodb-*/bin/mongod ${MONGODB_DIR}/bin/mongod
cp ${TEMP_MONGO}/mongodb-*/LICENSE-Community.txt ${MONGODB_DIR}/
chmod a+x ${MONGODB_DIR}/bin/mongod
rm -r ${TEMP_MONGO}

exit 0