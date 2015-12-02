#!/bin/bash

cd /var/monkey_island
openssl genrsa -out cc/server.key 1024
openssl req -new -key cc/server.key -out cc/server.csr
openssl x509 -req -days 366 -in cc/server.csr -signkey cc/server.key -out cc/server.crt
