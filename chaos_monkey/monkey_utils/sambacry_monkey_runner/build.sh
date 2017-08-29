gcc -c -Wall -Werror -fpic monkey_runner.c
gcc -shared -o monkey_runner.so monkey_runner.o