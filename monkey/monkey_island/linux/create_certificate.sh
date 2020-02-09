#!/bin/bash

server_root=${1:-"./cc"}


openssl genrsa -out $server_root/server.key 2048
openssl req -new -key $server_root/server.key -out $server_root/server.csr -subj "/C=GB/ST=London/L=London/O=Global Security/OU=Monkey Department/CN=monkey.com"
openssl x509 -req -days 366 -in $server_root/server.csr -signkey $server_root/server.key -out $server_root/server.crt

