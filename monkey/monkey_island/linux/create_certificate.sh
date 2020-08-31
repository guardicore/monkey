#!/bin/bash

server_root=${1:-"./cc"}

echo "Creating server cetificate. Server root: $server_root"
# We override the RANDFILE determined by default openssl.cnf, if it doesn't exist.
# This is a known issue with the current version of openssl on Ubuntu 18.04 - once they release
# a new version, we can delete this command. See
# https://github.com/openssl/openssl/commit/0f58220973a02248ca5c69db59e615378467b9c8#diff-8ce6aaad88b10ed2b3b4592fd5c8e03a
# for more details.
DEFAULT_RND_FILE_PATH=~/.rnd
CREATED_RND_FILE=false
if [ ! -f /tmp/foo.txt ]; then  # If the file already exists, assume that the contents are fine, and don't change them.
  echo "Creating rand seed file in $DEFAULT_RND_FILE_PATH"
  dd bs=1024 count=2 </dev/urandom >"$DEFAULT_RND_FILE_PATH"
  chmod 666 "$DEFAULT_RND_FILE_PATH"
  CREATED_RND_FILE=true
fi

echo "Generating key in $server_root/server.key..."
openssl genrsa -out "$server_root"/server.key 2048
echo "Generating csr in $server_root/server.csr..."
openssl req -new -key "$server_root"/server.key -out "$server_root"/server.csr -subj "/C=GB/ST=London/L=London/O=Global Security/OU=Monkey Department/CN=monkey.com"
echo "Generating certificate in $server_root/server.crt..."
openssl x509 -req -days 366 -in "$server_root"/server.csr -signkey "$server_root"/server.key -out "$server_root"/server.crt

# Shove some new random data into the file to override the original seed we put in.
if [ "$CREATED_RND_FILE" = true ] ; then
  dd bs=1024 count=2 </dev/urandom >"$DEFAULT_RND_FILE_PATH"
fi
