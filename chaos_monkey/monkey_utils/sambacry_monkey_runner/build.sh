#!/usr/bin/env bash
gcc -c -Wall -Werror -fpic -m64 sc_monkey_runner.c
gcc -shared -m64 -o sc_monkey_runner64.so sc_monkey_runner.o
rm sc_monkey_runner.o
strip sc_monkey_runner64.so
gcc -c -Wall -Werror -fpic -m32 sc_monkey_runner.c
gcc -shared -m32 -o sc_monkey_runner32.so sc_monkey_runner.o
rm sc_monkey_runner.o
strip sc_monkey_runner32.so