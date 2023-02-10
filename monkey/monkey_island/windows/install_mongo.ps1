param(
    [Parameter(Mandatory = $true, Position = 0)]
    [String]$binDir
)

$MONGODB_URL = "https://fastdl.mongodb.org/win32/mongodb-win32-x86_64-2012plus-4.2.20.zip"
$TEMP_MONGODB_ZIP = (Join-Path -path $(Get-Location) -ChildPath ".\mongodb.zip")


if (!(Test-Path -Path (Join-Path -Path $binDir -ChildPath "mongodb")))
    {
        "Downloading mongodb ..."
        [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
        (New-Object System.Net.WebClient).DownloadFile($MONGODB_URL, $TEMP_MONGODB_ZIP)

        "Unzipping mongodb"
        Expand-Archive $TEMP_MONGODB_ZIP -DestinationPath $binDir

        # Get unzipped folder's name
        $mongodb_folder_name = Get-ChildItem -Path $binDir | Where-Object -FilterScript {
            ($_.Name -like "mongodb*")
        } | Select-Object -ExpandProperty Name

        Write-Output $mongodb_folder_name

        # Move mongod file and license file from extracted folder to mongodb folder
        New-Item -ItemType directory -Path (Join-Path -Path $binDir -ChildPath "mongodb")
        "Moving extracted mongod and license files"
        $mongodb_folder_path = (Join-Path -Path $binDir -ChildPath $mongodb_folder_name)
        $mongodb_bin_folder_path = (Join-Path -Path $mongodb_folder_path -ChildPath "\bin\")
        $mongod_binary = (Join-Path -Path $mongodb_bin_folder_path -ChildPath "mongod.exe")
        $license_file = (Join-Path -Path $mongodb_folder_path -ChildPath "LICENSE-Community.txt")
        Move-Item -Path $mongod_binary -Destination (Join-Path -Path $binDir -ChildPath "mongodb\")
        Move-Item -Path $license_file -Destination (Join-Path -Path $binDir -ChildPath "mongodb\")

        "Removing zip file and folder with extracted contents"
        Remove-Item $TEMP_MONGODB_ZIP
        Remove-Item $mongodb_folder_path -Recurse
    }
