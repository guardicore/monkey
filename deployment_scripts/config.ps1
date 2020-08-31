# Absolute monkey's path
$MONKEY_FOLDER_NAME = "infection_monkey"
# Url of public git repository that contains monkey's source code
$MONKEY_REPO = "guardicore/monkey"
$MONKEY_GIT_URL = "https://github.com/guardicore/monkey"
$MONKEY_RELEASES_URL = $MONKEY_GIT_URL + "/releases"
$MONKEY_API_RELEASES_URL = "https://api.github.com/repos/$MONKEY_REPO/releases"
$MONKEY_LATEST_VERSION = (Invoke-WebRequest $MONKEY_API_RELEASES_URL | ConvertFrom-Json)[0].tag_name
$MONKEY_DOWNLOAD_URL = $MONKEY_RELEASES_URL + "/download/" + $MONKEY_LATEST_VERSION + "/"
# Link to the latest python download or install it manually
$PYTHON_URL = "https://www.python.org/ftp/python/3.7.7/python-3.7.7-amd64.exe"


# Monkey binaries
$LINUX_32_BINARY_URL = $MONKEY_DOWNLOAD_URL + "monkey-linux-32"
$LINUX_32_BINARY_PATH = "monkey-linux-32"
$LINUX_64_BINARY_URL = $MONKEY_DOWNLOAD_URL + "monkey-linux-64"
$LINUX_64_BINARY_PATH = "monkey-linux-64"
$WINDOWS_32_BINARY_URL = $MONKEY_DOWNLOAD_URL + "monkey-windows-32.exe"
$WINDOWS_32_BINARY_PATH = "monkey-windows-32.exe"
$WINDOWS_64_BINARY_URL = $MONKEY_DOWNLOAD_URL + "monkey-windows-64.exe"
$WINDOWS_64_BINARY_PATH = "monkey-windows-64.exe"
$SAMBA_32_BINARY_URL = $MONKEY_DOWNLOAD_URL + "sc_monkey_runner32.so"
$SAMBA_32_BINARY_NAME = "sc_monkey_runner32.so"
$SAMBA_64_BINARY_URL = $MONKEY_DOWNLOAD_URL + "sc_monkey_runner64.so"
$SAMBA_64_BINARY_NAME = "sc_monkey_runner64.so"
$TRACEROUTE_64_BINARY_URL = $MONKEY_DOWNLOAD_URL + "traceroute64"
$TRACEROUTE_32_BINARY_URL = $MONKEY_DOWNLOAD_URL + "traceroute32"

# Other directories and paths ( most likely you dont need to configure)
$MONKEY_ISLAND_DIR = Join-Path "\monkey" -ChildPath "monkey_island"
$MONKEY_DIR = Join-Path "\monkey" -ChildPath "infection_monkey"
$SAMBA_BINARIES_DIR = Join-Path -Path $MONKEY_DIR -ChildPath "\bin"
$TEMP_PYTHON_INSTALLER = ".\python.exe"
$TEMP_MONGODB_ZIP = ".\mongodb.zip"
$TEMP_OPEN_SSL_ZIP = ".\openssl.zip"
$TEMP_CPP_INSTALLER = "cpp.exe"
$TEMP_NPM_INSTALLER = "node.msi"
$TEMP_UPX_ZIP = "upx.zip"
$UPX_FOLDER = "upx-3.96-win64"

# Other url's
$MONGODB_URL = "https://downloads.mongodb.org/win32/mongodb-win32-x86_64-2012plus-v4.2-latest.zip"
$OPEN_SSL_URL = "https://indy.fulgan.com/SSL/openssl-1.0.2u-x64_86-win64.zip"
$CPP_URL = "https://go.microsoft.com/fwlink/?LinkId=746572"
$NPM_URL = "https://nodejs.org/dist/v12.14.1/node-v12.14.1-x64.msi"
$UPX_URL = "https://github.com/upx/upx/releases/download/v3.96/upx-3.96-win64.zip"
