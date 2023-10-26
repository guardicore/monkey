#!/bin/bash

NODE_VERSION="v20.7.0"
NODE_URL="https://nodejs.org/dist/$NODE_VERSION/node-$NODE_VERSION-linux-x64.tar.xz"

node_dir=$1

if ! [ -f "$node_dir/node" ]; then
    echo "Downloading node server"
    mkdir -p "$node_dir"
    curl -L "$NODE_URL" | tar -xJ -C "$node_dir" --strip=2 "node-$NODE_VERSION-linux-x64/bin/node"
else
    echo "Node server already exists."
fi
