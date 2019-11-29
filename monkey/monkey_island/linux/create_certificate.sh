#!/bin/bash

openssl genrsa -out ./cc/server.key 2048
openssl req -new -key ./cc/server.key -out ./cc/server.csr -subj "/OU=Monkey Department/CN=monkey.com"
openssl x509 -req -days 366 -in ./cc/server.csr -signkey ./cc/server.key -out ./cc/server.crt

