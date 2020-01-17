#include <windows.h>
#include <wininet.h>
#include <stdio.h>
#include <stdlib.h>

#pragma comment( lib, "wininet" )
#pragma comment (lib, "Wininet.lib")

int ping_island(int argc, char * argv[])
{
    DWORD dwVersion = 0;
    DWORD dwMajorVersion = 0;
    DWORD dwMinorVersion = 0;
    DWORD dwBuild = 0;

    dwVersion = GetVersion();

    // Get the Windows version.

    dwMajorVersion = (DWORD)(LOBYTE(LOWORD(dwVersion)));
    dwMinorVersion = (DWORD)(HIBYTE(LOWORD(dwVersion)));

    // Get the build number.

    if (dwVersion < 0x80000000)
        dwBuild = (DWORD)(HIWORD(dwVersion));

    char versionStr[20];
    snprintf(versionStr,
             20,
             "W%d.%d (%d)\n",
             dwMajorVersion,
             dwMinorVersion,
             dwBuild);


    wchar_t  _server[] = L"158.129.18.132";
    wchar_t _page[] = L"/api/bootloader";
    HINTERNET hInternet, hConnect, hRequest;
    DWORD bytes_read;
    int finished = 0;
    hInternet = InternetOpen("Mozilla/5.0", INTERNET_OPEN_TYPE_PRECONFIG, NULL, NULL, 0);
    if (hInternet == NULL) {
        printf("InternetOpen error : <%lu>\n", GetLastError());
        return 1;
    }

    hConnect = InternetConnect(hInternet, _server, 5000, "", "", INTERNET_SERVICE_HTTP, 0, 0);
    if (hConnect == NULL) {
        printf("hConnect error : <%lu>\n", GetLastError());
        return 1;
    }
    hRequest = HttpOpenRequest(hConnect, L"POST", _page, NULL, NULL, NULL, INTERNET_FLAG_SECURE, 0);
    if (hRequest == NULL) {
        printf("hRequest error : <%lu>\n", GetLastError());
        return 1;
    }


    DWORD dwFlags;
    DWORD dwBuffLen = sizeof(dwFlags);

    if (InternetQueryOption (hRequest, INTERNET_OPTION_SECURITY_FLAGS, &dwFlags, &dwBuffLen))
    {
        dwFlags |= SECURITY_FLAG_IGNORE_UNKNOWN_CA;
        dwFlags |= SECURITY_FLAG_IGNORE_CERT_CN_INVALID;
        InternetSetOption (hRequest, INTERNET_OPTION_SECURITY_FLAGS, &dwFlags, sizeof (dwFlags));
    }

    BOOL isSend = HttpSendRequest(hRequest, NULL, 0, versionStr, 20);
    if (!isSend){
        printf("HttpSendRequest error : (%lu)\n", GetLastError());
        return 1;
    }
    DWORD dwFileSize;
	dwFileSize = BUFSIZ;

	char buffer[BUFSIZ+1];

	while (1) {
		DWORD dwBytesRead;
		BOOL bRead;

		bRead = InternetReadFile(
			hRequest,
			buffer,
			dwFileSize + 1,
			&dwBytesRead);

		if (dwBytesRead == 0) break;

		if (!bRead) {
			printf("InternetReadFile error : <%lu>\n", GetLastError());
		}
		else {
			buffer[dwBytesRead] = 0;
			printf("Retrieved %lu data bytes: %s\n", dwBytesRead, buffer);
		}
	}

    // close request
    InternetCloseHandle(hRequest);
    InternetCloseHandle(hInternet);
    InternetCloseHandle(hConnect);

    return 0;
}
