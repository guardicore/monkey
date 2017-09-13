#!/usr/bin/env bash
gcc -c -Wall -Werror -fpic sc_monkey_runner.c
gcc -shared -o sc_monkey_runner.so sc_monkey_runner.o
