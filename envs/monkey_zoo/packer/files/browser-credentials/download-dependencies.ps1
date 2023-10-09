# Create a unique temporary directory
$tempDir = Join-Path ([IO.Path]::GetTempPath()) ([System.Guid]::NewGuid().ToString('n'))
$null = New-Item $tempDir -ItemType Directory

[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

# Download and extract BouncyCastle.Crypto.dll
$destinationDir = "C:\\Users\\m0nk3y\\Desktop"
$url = "https://www.bouncycastle.org/csharp/download/bccrypto-csharp-1.9.0-bin.zip"
$path = Join-Path $tempDir "bccrypto-csharp-1.9.0-bin.zip"
(New-Object System.Net.WebClient).DownloadFile($url, $path)
if ((Get-FileHash $path).Hash -ne "B3624908AB8FFDAE71495FDFB0E6F19206737221663625D88C61DDBEF42D7182")
{
    Write-Host "FAILED to validate BouncyCastle download."
    exit 1
}

Expand-Archive -Path $path -DestinationPath "C:\\Users\\m0nk3y\\Desktop" -Force


# Download and extract System.Data.SQLite.dll
$url = "https://system.data.sqlite.org/blobs/1.0.118.0/sqlite-netFx40-static-binary-bundle-x64-2010-1.0.118.0.zip"
$path = Join-Path $tempDir "sqlite.zip"
(New-Object System.Net.WebClient).DownloadFile($url, $path)
if ((Get-FileHash $path).Hash -ne "8166CDD111A01D01BE22558E50BC042EBA7ADAA2825DB31DB93FEE5A0D5245CA")
{
    Write-Host "FAILED to validate SQLite download."
    exit 1
}

try {
    # Extract archive to temp dir
    Expand-Archive -LiteralPath $path -DestinationPath $tempDir

    # Copy the file we are interested in
    $tempFilePath = Join-Path $tempDir "System.Data.SQLite.dll"
    Copy-Item $tempFilePath $destinationDir
}
finally {
    # Remove the temp dir
    if( Test-Path $tempDir ) {
        Remove-Item $tempDir -Recurse -Force -EA Continue
    }
}
