@echo off

IF [%1] == [] (
	set mydir=%cd%\
) ELSE (
	set mydir=%~1%
)

echo Monkey Island folder: %mydir%

SET OPENSSL_CONF=%mydir%bin\openssl\openssl.cfg
copy "%mydir%windows\openssl.cfg" "%mydir%bin\openssl\openssl.cfg"

@echo on

"%mydir%bin\openssl\openssl.exe" genrsa -out "%mydir%cc\server.key" 2048
"%mydir%bin\openssl\openssl.exe" req -new -config "%mydir%bin\openssl\openssl.cfg" -key "%mydir%cc\server.key" -out "%mydir%cc\server.csr" -subj "/OU=Monkey Department/CN=monkey.com"
"%mydir%bin\openssl\openssl.exe" x509 -req -days 366 -in "%mydir%cc\server.csr" -signkey "%mydir%cc\server.key" -out "%mydir%cc\server.crt"


:: Change file permissions
SET adminsIdentity="BUILTIN\Administrators"
FOR /f "delims=''" %%O IN ('whoami') DO SET ownIdentity=%%O

FOR %%F IN ("%mydir%cc\server.key", "%mydir%cc\server.csr", "%mydir%cc\server.crt") DO (

	:: Remove all others and add admins rule (with full control)
	echo y| cacls %%F /p %adminsIdentity%:F

	:: Add user rule (with read)
	echo y| cacls %%F /e /p "%ownIdentity%":R
)
