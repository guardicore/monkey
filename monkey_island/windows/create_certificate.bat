@echo off

SET OPENSSL_CONF=bin\openssl\openssl.cfg

IF [%1] == [] (
	set dir=%cd%\
) ELSE (
	set dir=%1
	REM - Remove double quotes -
	set dir=%dir:"=%
)

echo Monkey Island folder: %dir%

@echo on

"%dir%bin\openssl\openssl.exe" genrsa -out "%dir%cc\server.key" 1024
"%dir%bin\openssl\openssl.exe" req -new -config "%dir%bin\openssl\openssl.cfg" -key "%dir%cc\server.key" -out "%dir%cc\server.csr" -subj "/C=GB/ST=London/L=London/O=Global Security/OU=Monkey Department/CN=monkey.com"
"%dir%bin\openssl\openssl.exe" x509 -req -days 366 -in "%dir%cc\server.csr" -signkey "%dir%cc\server.key" -out "%dir%cc\server.crt"