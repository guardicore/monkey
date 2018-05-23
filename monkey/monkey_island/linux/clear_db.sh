#!/bin/bash

service monkey-mongo stop
cd /var/monkey/monkey_island
rm -rf ./db/*
service monkey-mongo start
