# Absolute monkey's path
$MONKEY_FOLDER_NAME = "infection_monkey"
# Url of public git repository that contains monkey's source code
$MONKEY_GIT_URL = "https://github.com/guardicore/monkey"
# Link to the latest python download or install it manually
$PYTHON_URL = "https://www.python.org/ftp/python/3.7.4/python-3.7.4-amd64.exe"

# Monkey binaries
$LINUX_32_BINARY_URL = "https://github.com/guardicore/monkey/releases/download/1.6/monkey-linux-32"
$LINUX_32_BINARY_PATH = "monkey-linux-32"
$LINUX_64_BINARY_URL = "https://github.com/guardicore/monkey/releases/download/1.6/monkey-linux-64"
$LINUX_64_BINARY_PATH = "monkey-linux-64"
$WINDOWS_32_BINARY_URL = "https://github.com/guardicore/monkey/releases/download/1.6/monkey-windows-32.exe"
$WINDOWS_32_BINARY_PATH = "monkey-windows-32.exe"
$WINDOWS_64_BINARY_URL = "https://github.com/guardicore/monkey/releases/download/1.6/monkey-windows-64.exe"
$WINDOWS_64_BINARY_PATH = "monkey-windows-64.exe"
$SAMBA_32_BINARY_URL = "https://github.com/VakarisZ/tempBinaries/raw/master/sc_monkey_runner32.so"
$SAMBA_32_BINARY_NAME= "sc_monkey_runner32.so"
$SAMBA_64_BINARY_URL = "https://github.com/VakarisZ/tempBinaries/raw/master/sc_monkey_runner64.so"
$SAMBA_64_BINARY_NAME = "sc_monkey_runner64.so"

# Other directories and paths ( most likely you dont need to configure)
$MONKEY_ISLAND_DIR = "\monkey\monkey_island"
$MONKEY_DIR = "\monkey\infection_monkey"
$SAMBA_BINARIES_DIR = Join-Path -Path $MONKEY_DIR -ChildPath "\exploit\sambacry_monkey_runner"
$PYTHON_DLL = "C:\Windows\System32\python27.dll"
$MK32_DLL = "mk32.dll"
$MK64_DLL = "mk64.dll"
$TEMP_PYTHON_INSTALLER = ".\python.msi"
$TEMP_MONGODB_ZIP = ".\mongodb.zip"
$TEMP_OPEN_SSL_ZIP = ".\openssl.zip"
$TEMP_CPP_INSTALLER = "cpp.exe"
$TEMP_NPM_INSTALLER = "node.msi"
$TEMP_PYWIN32_INSTALLER = "pywin32.exe"
$TEMP_UPX_ZIP = "upx.zip"
$UPX_FOLDER = "upx394w"

# Other url's
$MONGODB_URL = "https://downloads.mongodb.org/win32/mongodb-win32-x86_64-2008plus-ssl-latest.zip"
$OPEN_SSL_URL = "https://indy.fulgan.com/SSL/Archive/openssl-1.0.2l-i386-win32.zip"
$NPM_URL = "https://nodejs.org/dist/v10.13.0/node-v10.13.0-x64.msi"
$PYWIN32_URL = "https://github.com/mhammond/pywin32/releases/download/b224/pywin32-224.win-amd64-py2.7.exe"
$UPX_URL = "https://github.com/upx/upx/releases/download/v3.94/upx394w.zip"
$MK32_DLL_URL = "https://github.com/guardicore/mimikatz/releases/download/1.1.0/mk32.dll"
$MK64_DLL_URL = "https://github.com/guardicore/mimikatz/releases/download/1.1.0/mk64.dll"
