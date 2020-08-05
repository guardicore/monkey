param(
    [Parameter(Mandatory = $false, Position = 0)]
    [String] $monkey_home = (Get-Item -Path ".\").FullName,

    [Parameter(Mandatory = $false, Position = 1)]
    [System.String]
    $branch = "develop",
    [Parameter(Mandatory = $false, Position = 2)]
    [Bool]
    $agents = $true
)
function Deploy-Windows([String] $monkey_home = (Get-Item -Path ".\").FullName, [String] $branch = "develop")
{
    Write-Output "Downloading to $monkey_home"
    Write-Output "Branch $branch"
    # Set variables for script execution
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    $webClient = New-Object System.Net.WebClient


    # Import the config variables
    $config_filename = New-TemporaryFile
    $config_filename = "config.ps1"
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


    # We check if git is installed
    try
    {
        git | Out-Null -ErrorAction Stop
        "Git requirement satisfied"
    }
    catch [System.Management.Automation.CommandNotFoundException]
    {
        "Please install git before running this script or add it to path and restart cmd"
        return
    }

    # Download the monkey
    $command = "git clone --single-branch --recurse-submodules -b $branch $MONKEY_GIT_URL $monkey_home 2>&1"
    Write-Output $command
    $output = cmd.exe /c $command
    $binDir = (Join-Path -Path $monkey_home -ChildPath $MONKEY_ISLAND_DIR | Join-Path -ChildPath "\bin")
    if ($output -like "*already exists and is not an empty directory.*")
    {
        "Assuming you already have the source directory. If not, make sure to set an empty directory as monkey's home directory."
    }
    elseif ($output -like "fatal:*")
    {
        "Error while cloning monkey from the repository:"
        $output
        return
    }
    else
    {
        "Monkey cloned from the repository"
        # Create bin directory
        New-Item -ItemType directory -path $binDir
        "Bin directory added"
    }

    # We check if python is installed
    try
    {
        $version = cmd.exe /c '"python" --version  2>&1'
        if ($version -like 'Python 3.*')
        {
            "Python 3.* was found, installing dependencies"
        }
        else
        {
            throw System.Management.Automation.CommandNotFoundException
        }
    }
    catch [System.Management.Automation.CommandNotFoundException]
    {
        "Downloading python 3 ..."
        "Select 'add to PATH' when installing"
        $webClient.DownloadFile($PYTHON_URL, $TEMP_PYTHON_INSTALLER)
        Start-Process -Wait $TEMP_PYTHON_INSTALLER -ErrorAction Stop
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
        Remove-Item $TEMP_PYTHON_INSTALLER
        # Check if installed correctly
        $version = cmd.exe /c '"python" --version  2>&1'
        if ($version -like '* is not recognized*')
        {
            "Python is not found in PATH. Add it to PATH and relaunch the script."
            return
        }
    }

    "Upgrading pip..."
    $output = cmd.exe /c 'python -m pip install --user --upgrade pip 2>&1'
    $output
    if ($output -like '*No module named pip*')
    {
        "Make sure pip module is installed and re-run this script."
        return
    }

    "Installing python packages for island"
    $islandRequirements = Join-Path -Path $monkey_home -ChildPath $MONKEY_ISLAND_DIR | Join-Path -ChildPath "\requirements.txt" -ErrorAction Stop
    & python -m pip install --user -r $islandRequirements
    "Installing python packages for monkey"
    $monkeyRequirements = Join-Path -Path $monkey_home -ChildPath $MONKEY_DIR | Join-Path -ChildPath "\requirements.txt"
    & python -m pip install --user -r $monkeyRequirements

    $user_python_dir = cmd.exe /c 'py -m site --user-site'
    $user_python_dir = Join-Path (Split-Path $user_python_dir) -ChildPath "\Scripts"
    if (!($ENV:Path | Select-String -SimpleMatch $user_python_dir))
    {
        "Adding python scripts path to user's env"
        $env:Path += ";" + $user_python_dir
        [Environment]::SetEnvironmentVariable("Path", $env:Path, "User")
    }

    # Download mongodb
    if (!(Test-Path -Path (Join-Path -Path $binDir -ChildPath "mongodb")))
    {
        "Downloading mongodb ..."
        $webClient.DownloadFile($MONGODB_URL, $TEMP_MONGODB_ZIP)
        "Unzipping mongodb"
        Expand-Archive $TEMP_MONGODB_ZIP -DestinationPath $binDir
        # Get unzipped folder's name
        $mongodb_folder = Get-ChildItem -Path $binDir | Where-Object -FilterScript {
            ($_.Name -like "mongodb*")
        } | Select-Object -ExpandProperty Name
        # Move all files from extracted folder to mongodb folder
        New-Item -ItemType directory -Path (Join-Path -Path $binDir -ChildPath "mongodb")
        New-Item -ItemType directory -Path (Join-Path -Path $monkey_home -ChildPath $MONKEY_ISLAND_DIR | Join-Path -ChildPath "db")
        "Moving extracted files"
        Move-Item -Path (Join-Path -Path $binDir -ChildPath $mongodb_folder | Join-Path -ChildPath "\bin\*") -Destination (Join-Path -Path $binDir -ChildPath "mongodb\")
        "Removing zip file"
        Remove-Item $TEMP_MONGODB_ZIP
        Remove-Item (Join-Path -Path $binDir -ChildPath $mongodb_folder) -Recurse
    }

    # Download OpenSSL
    "Downloading OpenSSL ..."
    $webClient.DownloadFile($OPEN_SSL_URL, $TEMP_OPEN_SSL_ZIP)
    "Unzipping OpenSSl"
    Expand-Archive $TEMP_OPEN_SSL_ZIP -DestinationPath (Join-Path -Path $binDir -ChildPath "openssl") -ErrorAction SilentlyContinue
    "Removing zip file"
    Remove-Item $TEMP_OPEN_SSL_ZIP

    # Download and install C++ redistributable
    "Downloading C++ redistributable ..."
    $webClient.DownloadFile($CPP_URL, $TEMP_CPP_INSTALLER)
    Start-Process -Wait $TEMP_CPP_INSTALLER -ErrorAction Stop
    Remove-Item $TEMP_CPP_INSTALLER

    # Generate ssl certificate
    "Generating ssl certificate"
    Push-Location -Path (Join-Path -Path $monkey_home -ChildPath $MONKEY_ISLAND_DIR)
    . .\windows\create_certificate.bat
    Pop-Location

    if ($agents)
    {
        # Adding binaries
        "Adding binaries"
        $binaries = (Join-Path -Path $monkey_home -ChildPath $MONKEY_ISLAND_DIR | Join-Path -ChildPath "\cc\binaries")
        New-Item -ItemType directory -path $binaries -ErrorAction SilentlyContinue
        $webClient.DownloadFile($LINUX_32_BINARY_URL, (Join-Path -Path $binaries -ChildPath $LINUX_32_BINARY_PATH))
        $webClient.DownloadFile($LINUX_64_BINARY_URL, (Join-Path -Path $binaries -ChildPath $LINUX_64_BINARY_PATH))
        $webClient.DownloadFile($WINDOWS_32_BINARY_URL, (Join-Path -Path $binaries -ChildPath $WINDOWS_32_BINARY_PATH))
        $webClient.DownloadFile($WINDOWS_64_BINARY_URL, (Join-Path -Path $binaries -ChildPath $WINDOWS_64_BINARY_PATH))
    }


    # Check if NPM installed
    "Installing npm"
    try
    {
        $version = cmd.exe /c '"npm" --version  2>&1'
        if ($version -like "*is not recognized*")
        {
            throw System.Management.Automation.CommandNotFoundException
        }
        else
        {
            "Npm already installed"
        }
    }
    catch [System.Management.Automation.CommandNotFoundException]
    {
        "Downloading npm ..."
        $webClient.DownloadFile($NPM_URL, $TEMP_NPM_INSTALLER)
        Start-Process -Wait $TEMP_NPM_INSTALLER
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine")
        Remove-Item $TEMP_NPM_INSTALLER
    }

    "Updating npm"
    Push-Location -Path (Join-Path -Path $monkey_home -ChildPath $MONKEY_ISLAND_DIR | Join-Path -ChildPath "\cc\ui")
    & npm update
    & npm run dist
    Pop-Location

    # Create infection_monkey/bin directory if not already present
    $binDir = (Join-Path -Path $monkey_home -ChildPath $MONKEY_DIR | Join-Path -ChildPath "\bin")
    New-Item -ItemType directory -path $binaries -ErrorAction SilentlyContinue

    # Download upx
    if (!(Test-Path -Path (Join-Path -Path $binDir -ChildPath "upx.exe")))
    {
        "Downloading upx ..."
        $webClient.DownloadFile($UPX_URL, $TEMP_UPX_ZIP)
        "Unzipping upx"
        Expand-Archive $TEMP_UPX_ZIP -DestinationPath $binDir -ErrorAction SilentlyContinue
        Move-Item -Path (Join-Path -Path $binDir -ChildPath $UPX_FOLDER | Join-Path -ChildPath "upx.exe") -Destination $binDir
        # Remove unnecessary files
        Remove-Item -Recurse -Force (Join-Path -Path $binDir -ChildPath $UPX_FOLDER)
        "Removing zip file"
        Remove-Item $TEMP_UPX_ZIP
    }

    # Download sambacry binaries
    $samba_path = Join-Path -Path $monkey_home -ChildPath $SAMBA_BINARIES_DIR
    $samba32_path = Join-Path -Path $samba_path -ChildPath $SAMBA_32_BINARY_NAME
    if (!(Test-Path -Path $samba32_path))
    {
        "Downloading sambacry 32 binary"
        $webClient.DownloadFile($SAMBA_32_BINARY_URL, $samba32_path)
    }
    $samba64_path = Join-Path -Path $samba_path -ChildPath $SAMBA_64_BINARY_NAME
    if (!(Test-Path -Path $samba64_path))
    {
        "Downloading sambacry 64 binary"
        $webClient.DownloadFile($SAMBA_64_BINARY_URL, $samba64_path)
    }

    "Script finished"

}
Deploy-Windows -monkey_home $monkey_home -branch $branch
