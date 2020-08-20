$TEMP_FILE = 'monkey-timestomping-file.txt'
$TIMESTAMP_EPOCH = '01/01/1970 00:00:00'

# create temporary file
New-Item -Path $TEMP_FILE -Force | Out-Null
Set-Content $TEMP_FILE -Value "Successfully changed a file's modification timestamp" -Force | Out-Null

# attempt to change modification timestamp
Get-ChildItem $TEMP_FILE | % { $_.LastWriteTime = $TIMESTAMP_EPOCH }
Get-Content  $TEMP_FILE

# remove temporary file
Remove-Item $TEMP_FILE -Force -ErrorAction Ignore
