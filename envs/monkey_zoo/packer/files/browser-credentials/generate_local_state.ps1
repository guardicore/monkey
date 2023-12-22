# Check that the local state file has the required profile information
function local_state_updated() {
    try {
        $local_state = Get-Content "$env:LOCALAPPDATA\Google\Chrome\User Data\Local State" | ConvertFrom-Json
        return "Default" -in $local_state.profile.info_cache.PSObject.Properties.Name
    }
    catch {
        return $false
    }
}

$process = Start-Process "C:\Program Files\Google\Chrome\Application\chrome.exe" -ArgumentList "--no-first-run" -PassThru

# Wait for the local state file to be updated
while (-not (local_state_updated)){
    sleep -Seconds 1
}

Stop-Process $process.Id
