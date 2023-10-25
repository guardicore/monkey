# Absolute monkey's path
$MONKEY_FOLDER_NAME = "infection_monkey"
# Url of public git repository that contains monkey's source code
$MONKEY_REPO = "guardicore/monkey"
$MONKEY_GIT_URL = "https://github.com/guardicore/monkey"
$MONKEY_RELEASES_URL = $MONKEY_GIT_URL + "/releases"
$MONKEY_API_RELEASES_URL = "https://api.github.com/repos/$MONKEY_REPO/releases"
$MONKEY_LATEST_VERSION = (Invoke-WebRequest $MONKEY_API_RELEASES_URL -UseBasicParsing | ConvertFrom-Json)[0].tag_name
$MONKEY_DOWNLOAD_URL = "$MONKEY_RELEASES_URL/download/$MONKEY_LATEST_VERSION/"
$MONKEY_PYTHON_VERSION = "3.11.2"
$PYTHON_VERSION_REGEX = 'Python 3.11(\.(\d+))?$'
# Link to the latest python download or install it manually
$PYTHON_URL = "https://www.python.org/ftp/python/$MONKEY_PYTHON_VERSION/python-$MONKEY_PYTHON_VERSION-amd64.exe"

# Monkey binaries
$LINUX_64_BINARY_URL = $MONKEY_DOWNLOAD_URL + "monkey-linux-64"
$LINUX_64_BINARY_PATH = "monkey-linux-64"
$WINDOWS_64_BINARY_URL = $MONKEY_DOWNLOAD_URL + "monkey-windows-64.exe"
$WINDOWS_64_BINARY_PATH = "monkey-windows-64.exe"

# Other directories and paths ( most likely you dont need to configure)
$MONKEY_ISLAND_DIR = Join-Path "\monkey" -ChildPath "monkey_island"
$MONKEY_DIR = Join-Path "\monkey" -ChildPath "infection_monkey"
$TEMP_PYTHON_INSTALLER = ".\python.exe"
$TEMP_OPEN_SSL_ZIP = ".\openssl.zip"
$TEMP_CPP_INSTALLER = "cpp.exe"
$TEMP_NPM_INSTALLER = "node.msi"
$TEMP_UPX_ZIP = "upx.zip"
$UPX_FOLDER = "upx-3.96-win64"

# Other url's
$OPEN_SSL_URL = "https://indy.fulgan.com/SSL/openssl-1.0.2u-x64_86-win64.zip"
$CPP_URL = "https://go.microsoft.com/fwlink/?LinkId=746572"
$NPM_URL = "https://nodejs.org/dist/v20.7.0/node-v20.7.0-x64.msi"
$UPX_URL = "https://github.com/upx/upx/releases/download/v3.96/upx-3.96-win64.zip"
