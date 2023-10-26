param(
    [Parameter(Mandatory = $true, Position = 0)]
    [String]$destinationDir
)

function Create-TempDir()
{
    $tempDir = Join-Path ([IO.Path]::GetTempPath()) ([System.Guid]::NewGuid().ToString('n'))
    New-Item $tempDir -ItemType Directory
}

function Extract-SingleFile([String] $archivePath, [String] $fileToExtract, [String] $destinationDir)
{
    Add-Type -Assembly System.IO.Compression.Filesystem
    $archive = [IO.Compression.ZipFile]::OpenRead( $archivePath )
    try {
        if( $foundFile = $archive.GetEntry($fileToExtract) ) {
            $destinationFile = Join-Path $destinationDir $foundFile.Name
            [IO.Compression.ZipFileExtensions]::ExtractToFile( $foundFile, $destinationFile )
        }
        else {
            Write-Error "File not found in ZIP: $fileToExtract"
        }
    }
    finally {
        # Dispose the archive so the file will be unlocked again.
        if( $archive ) {
            $archive.Dispose()
        }
    }
}

$NODE_VERSION = "v20.7.0"
$NODE_ZIP_FILENAME = "node-$NODE_VERSION-win-x64.zip"
$NODE_URL = "https://nodejs.org/dist/$NODE_VERSION/node-$NODE_VERSION-win-x64.zip"

if (!(Test-Path -Path (Join-Path $destinationDir "node.exe") -PathType Leaf))
{
    "Downloading node server ..."
    md -Force $destinationDir | Out-Null
    $tempDir = Create-TempDir
    $archivePath = Join-Path $tempDir $NODE_ZIP_FILENAME
    try {
        (New-Object System.Net.WebClient).DownloadFile($NODE_URL, $archivePath)
        Extract-SingleFile $archivePath "node-$NODE_VERSION-win-x64/node.exe" $destinationDir
    }
    finally {
        rmdir $tempDir -r -force
    }
}
else
{
    "Node server already exists."
}
