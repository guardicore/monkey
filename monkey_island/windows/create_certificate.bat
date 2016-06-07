C:\OpenSSL-Win64\bin\openssl.exe genrsa -out cc\server.key 1024
C:\OpenSSL-Win64\bin\openssl.exe req -new -config C:\OpenSSL-Win64\bin\openssl.cfg -key cc\server.key -out cc\server.csr -subj "/C=GB/ST=London/L=London/O=Global Security/OU=Monkey Department/CN=monkey.com"
C:\OpenSSL-Win64\bin\openssl.exe x509 -req -days 366 -in cc\server.csr -signkey cc\server.key -out cc\server.crt
pause