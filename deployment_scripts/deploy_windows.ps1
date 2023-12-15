param(
    [Parameter(Mandatory = $false, Position = 0)]
    [String] $monkey_home = (Get-Item -Path ".\").FullName,

    [Parameter(Mandatory = $false, Position = 1)]
    [String] $branch = "develop",

    [Parameter(Mandatory = $false, Position = 2)]
    [Bool] $agents = $true
)

$ESCAPE = "$([char]27)"
$BOLD = "$ESCAPE[1m"
$CYAN = "$ESCAPE[36m"
$RESET = "$ESCAPE[0m"

function Print-Status([Parameter(Mandatory = $true)] [string]$Text)
{
    Write-Output "$($BOLD)$($CYAN)$Text$($RESET)"
}

function Assert-CommandExists($command)
{
    try
    {
        Get-Command $command -ErrorAction Stop | Out-Null
    }
    catch [System.Management.Automation.CommandNotFoundException]
    {
        Write-Output "Command does not exist: $command"
        Write-Output "Please install $command or add it to path before running this script"
        exit 1
    }
}

function Clone-MonkeyRepo([String] $DestinationPath, [String] $Branch)
{
    $command = "git clone --single-branch --recurse-submodules -b $Branch $MONKEY_GIT_URL $DestinationPath 2>&1"
    Write-Output $command
    $output = cmd.exe /c $command
    if ($output -like "*already exists and is not an empty directory.*")
    {
        "Assuming you already have the source directory. If not, make sure to set an empty directory as monkey's home directory."
    }
    elseif ($output -like "fatal:*")
    {
        "Error while cloning monkey from the repository:"
        $output
        exit 1
    }
    else
    {
        "Monkey cloned from the repository"
    }
}

function Install-Python
{
    try
    {
        $version = python --version  2>&1
        if ($version -notmatch $PYTHON_VERSION_REGEX -or $Matches.2 -lt 2)
        {
            throw System.Management.Automation.CommandNotFoundException
        }
    }
    catch [System.Management.Automation.CommandNotFoundException]
    {
        "Downloading python $MONKEY_PYTHON_VERSION ..."
        "Select 'add to PATH' when installing"
        $webClient.DownloadFile($PYTHON_URL, $TEMP_PYTHON_INSTALLER)
        Start-Process -Wait $TEMP_PYTHON_INSTALLER -ErrorAction Stop
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
        Remove-Item $TEMP_PYTHON_INSTALLER
        # Check if installed correctly
        $version = python --version  2>&1
        if ($version -like '* is not recognized*')
        {
            "Python is not found in PATH. Add it to PATH and relaunch the script."
            exit 1
        }
    }
}

function Configure-precommit([String] $git_repo_dir)
{
    Print-Status "Installing pre-commit and setting up pre-commit hook"
    Push-Location $git_repo_dir
    python -m pip install pre-commit
	if ($LastExitCode) {
		exit 1
	}
    pre-commit install -t pre-commit -t pre-push -t prepare-commit-msg
	if ($LastExitCode) {
		exit 1
	}
    Pop-Location

    Print-Status "Pre-commit successfully installed"
}

function Install-NPM
{
    Print-Status "Installing npm"
    try
    {
        Get-Command npm -ErrorAction Stop | Out-Null
        "Npm already installed"
    }
    catch [System.Management.Automation.CommandNotFoundException]
    {
        "Downloading npm ..."
        $webClient.DownloadFile($NPM_URL, $TEMP_NPM_INSTALLER)
        Start-Process -Wait $TEMP_NPM_INSTALLER
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine")
        Remove-Item $TEMP_NPM_INSTALLER
    }
}

function Download-UPX([String] $DestinationPath)
{
    Print-Status "Downloading upx ..."
    $webClient.DownloadFile($UPX_URL, $TEMP_UPX_ZIP)
    "Unzipping upx"
    Expand-Archive $TEMP_UPX_ZIP -DestinationPath $DestinationPath -ErrorAction SilentlyContinue
    Move-Item -Path (Join-Path -Path $DestinationPath -ChildPath $UPX_FOLDER | Join-Path -ChildPath "upx.exe") -Destination $DestinationPath
    # Remove unnecessary files
    Remove-Item -Recurse -Force (Join-Path -Path $DestinationPath -ChildPath $UPX_FOLDER)
    "Removing zip file"
    Remove-Item $TEMP_UPX_ZIP
}

function Deploy-Windows([String] $monkey_home = (Get-Item -Path ".\").FullName, [String] $branch = "develop")
{
    Print-Status "Downloading to $monkey_home"
    Print-Status "Branch $branch"
    # Set variables for script execution
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    $webClient = New-Object System.Net.WebClient


    # Import the config variables
    $config_filename = New-TemporaryFile
    $config_filename = "$PsScriptRoot\config.ps1"
    $config_url = "https://raw.githubusercontent.com/guardicore/monkey/" + $branch + "/deployment_scripts/config.ps1"
    $webClient.DownloadFile($config_url, $config_filename)
    . ./config.ps1
    "Config variables from config.ps1 imported"
    Remove-Item $config_filename


    # If we want monkey in current dir we need to create an empty folder for source files
    if ((Join-Path $monkey_home '') -eq (Join-Path (Get-Item -Path ".\").FullName ''))
    {
        $monkey_home = Join-Path -Path $monkey_home -ChildPath $MONKEY_FOLDER_NAME
    }


    # Check if git is installed
    Assert-CommandExists git
    Clone-MonkeyRepo $monkey_home -Branch $branch
    Install-Python
    "$(python --version) is installed"

    Print-Status "Upgrading pip..."
    $output = cmd.exe /c 'python -m pip install --user --upgrade pip 2>&1'
    $output
    if ($output -like '*No module named pip*')
    {
        "Make sure pip module is installed and re-run this script."
        exit 1
    }

    Print-Status "Installing pipx"
    pip install --user -U pipx
    pipx ensurepath
    pipx install pipenv

    Print-Status "Installing python packages for island"
    Push-Location -Path (Join-Path -Path $monkey_home -ChildPath $MONKEY_ISLAND_DIR) -ErrorAction Stop
    pipenv install --dev
    Pop-Location
    Print-Status "Installing python packages for monkey"
    Push-Location -Path (Join-Path -Path $monkey_home -ChildPath $MONKEY_DIR) -ErrorAction Stop
    pipenv install --dev
    Pop-Location

    Configure-precommit($monkey_home)

    $user_python_dir = cmd.exe /c 'py -m site --user-site'
    $user_python_dir = Join-Path (Split-Path $user_python_dir) -ChildPath "\Scripts"
    if (!($ENV:Path | Select-String -SimpleMatch $user_python_dir))
    {
        "Adding python scripts path to user's env"
        $env:Path += ";" + $user_python_dir
        [Environment]::SetEnvironmentVariable("Path", $env:Path, "User")
    }

    $binDir = (Join-Path -Path $monkey_home -ChildPath $MONKEY_ISLAND_DIR | Join-Path -ChildPath "\bin")
    New-Item -ItemType directory -path $binDir
    $install_mongo_script = (Join-Path -Path $monkey_home -ChildPath "$MONKEY_ISLAND_DIR\windows\install_mongo.ps1")
    Invoke-Expression "$install_mongo_script -binDir $binDir"

    $install_node_script = (Join-Path -Path $monkey_home -ChildPath "$MONKEY_ISLAND_DIR\windows\install_node.ps1")
    $node_server_dir = (Join-Path -Path $binDir -ChildPath "node")
    Invoke-Expression "$install_node_script -destinationDir $node_server_dir"

    # Download OpenSSL
    Print-Status "Downloading OpenSSL ..."
    $webClient.DownloadFile($OPEN_SSL_URL, $TEMP_OPEN_SSL_ZIP)
    "Unzipping OpenSSl"
    Expand-Archive $TEMP_OPEN_SSL_ZIP -DestinationPath (Join-Path -Path $binDir -ChildPath "openssl") -ErrorAction SilentlyContinue
    "Removing zip file"
    Remove-Item $TEMP_OPEN_SSL_ZIP

    # Download and install C++ redistributable
    Print-Status "Downloading C++ redistributable ..."
    $webClient.DownloadFile($CPP_URL, $TEMP_CPP_INSTALLER)
    Start-Process -Wait $TEMP_CPP_INSTALLER -ErrorAction Stop
    Remove-Item $TEMP_CPP_INSTALLER

    # Generate ssl certificate
    Print-Status "Generating ssl certificate"
    Push-Location -Path (Join-Path -Path $monkey_home -ChildPath $MONKEY_ISLAND_DIR)
    . .\windows\create_certificate.bat
    Pop-Location

    if ($agents)
    {
        # Adding binaries
        Print-Status "Downloading agent binaries"
        $binaries = (Join-Path -Path $monkey_home -ChildPath $MONKEY_ISLAND_DIR | Join-Path -ChildPath "\cc\binaries")
        New-Item -ItemType directory -path $binaries -ErrorAction SilentlyContinue
        $webClient.DownloadFile($LINUX_64_BINARY_URL, (Join-Path -Path $binaries -ChildPath $LINUX_64_BINARY_PATH))
        $webClient.DownloadFile($WINDOWS_64_BINARY_URL, (Join-Path -Path $binaries -ChildPath $WINDOWS_64_BINARY_PATH))
    }


    # Check if NPM installed
    Install-NPM

    Print-Status "Updating npm"
    Push-Location -Path (Join-Path -Path $monkey_home -ChildPath $MONKEY_ISLAND_DIR | Join-Path -ChildPath "\cc\ui")
    & npm update
    & npm run build
    Pop-Location

    # Create infection_monkey/bin directory if not already present
    $binDir = (Join-Path -Path $monkey_home -ChildPath $MONKEY_DIR | Join-Path -ChildPath "\bin")
    New-Item -ItemType directory -path $binaries -ErrorAction SilentlyContinue

    # Download upx
    if (!(Test-Path -Path (Join-Path -Path $binDir -ChildPath "upx.exe")))
    {
        Download-UPX $binDir
    }


    Print-Status "Script finished"

}
Deploy-Windows -monkey_home $monkey_home -branch $branch
