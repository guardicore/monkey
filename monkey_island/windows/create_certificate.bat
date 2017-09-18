bin\openssl\openssl.exe genrsa -out cc\server.key 1024
bin\openssl\openssl.exe req -new -config bin\openssl\openssl.cfg -key cc\server.key -out cc\server.csr -subj "/C=GB/ST=London/L=London/O=Global Security/OU=Monkey Department/CN=monkey.com"
bin\openssl\openssl.exe x509 -req -days 366 -in cc\server.csr -signkey cc\server.key -out cc\server.crt