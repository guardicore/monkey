.\ci_scripts\validation-env\Scripts\activate.ps1
$ErrorActionPreference = "Stop"
python -m pip install -r monkey/monkey_island/requirements.txt
python -m pip install -r monkey/infection_monkey/requirements.txt
flake8 ./monkey --config ./ci_scripts/flake8_syntax_check.cfg
flake8 ./monkey --exit-zero --config ./ci_scripts/flake8_linter_check.cfg | Out-File -FilePath .\ci_scripts\flake8_warnings.txt
Get-Content -Path .\ci_scripts\flake8_warnings.txt
$PYTHON_WARNINGS_AMOUNT_UPPER_LIMIT = 80
if ((Get-Item -Path .\ci_scripts\flake8_warnings.txt | Get-Content -Tail 1) -gt $PYTHON_WARNINGS_AMOUNT_UPPER_LIMIT){
    "Too many python linter warnings! Failing this build. Lower the amount of linter errors in this and try again. "
    exit
}
python -m isort ./monkey -c --settings-file ./ci_scripts/isort.cfg
if (!$?) {
    $confirmation = Read-Host "Isort found errors. Do you want to attmpt to fix them automatically? (y/n)"
    if ($confirmation -eq 'y') {
        python -m isort ./monkey --settings-file ./ci_scripts/isort.cfg
    }
}
Push-Location -Path ./monkey
python ./monkey_island/cc/environment/set_server_config.py testing
python -m pytest
$lastCommandSucceeded = $?
python ./monkey_island/cc/environment/set_server_config.py restore
Pop-Location

if (!$lastCommandSucceeded) {
    exit
}

Push-Location -Path .\monkey\monkey_island\cc\ui
eslint ./src -c ./.eslintrc
Pop-Location

swimm verify

Write-Host "Script finished. Press any key to continue"
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown');
deactivate
