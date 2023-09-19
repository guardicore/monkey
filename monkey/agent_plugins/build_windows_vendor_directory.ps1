param(
  [Parameter(Mandatory = $true)] [string]$workspace,
  [Parameter(Mandatory = $true)] [string]$plugin_type,
  [Parameter(Mandatory = $true)] [string]$plugin_directory_name
)
Set-PSDebug -Trace 1

$plugin_path = Join-Path -Path $workspace -ChildPath "\monkey\monkey\agent_plugins\$plugin_type\$plugin_directory_name"

Write-Output "Building Windows vendor directory"

Set-Location $plugin_path

Remove-Item "$workspace\vendor-windows.zip" -Force
Remove-Item $plugin_path\venv -Recurse -Force
Remove-Item "$plugin_path\src\vendor-windows" -Recurse -Force
& python -m venv "$plugin_path\venv"
& "$plugin_path\venv\Scripts\Activate.ps1"

Write-Output "Python version: $(python --version)"
python -m pip install --upgrade pip
python -m pip install pipenv

pipenv sync

pipenv requirements >> requirements.txt
pip install -r requirements.txt -t src/vendor-windows
rm requirements.txt

#exit venv
deactivate

# The Compress-Archive command is stupidly slow with debugging turned on. Turn it off temporarily.
Set-PSDebug -Off
Compress-Archive -Path "$plugin_path\src\vendor-windows" -Destination "$workspace\vendor-windows.zip" -Force
Set-PSDebug -Trace 1

Remove-Item $plugin_path\venv -Recurse -Force
Remove-Item "$plugin_path\src\vendor-windows" -Recurse -Force
