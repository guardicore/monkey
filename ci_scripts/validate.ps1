.\ci_scripts\validation-env\Scripts\activate.ps1
flake8 ./monkey --config ./ci_scripts/flake8_syntax_check.cfg
flake8 ./monkey --exit-zero --config ./ci_scripts/flake8_linter_check.cfg | Out-File -FilePath .\ci_scripts\flake8_warnings.txt
Get-Content -Path .\ci_scripts\flake8_warnings.txt
$PYTHON_WARNINGS_AMOUNT_UPPER_LIMIT = 80
if ((Get-Item -Path .\ci_scripts\flake8_warnings.txt | Get-Content -Tail 1) -gt $PYTHON_WARNINGS_AMOUNT_UPPER_LIMIT){
    "Too many python linter warnings! Failing this build. Lower the amount of linter errors in this and try again. "
    exit
}
python -m isort ./monkey -c --settings-file ./ci_scripts/isort.cfg
# python -m isort ./monkey --settings-file ./ci_scripts/isort.cfg
python monkey_island/cc/environment/set_server_config.py testing
python -m pytest
Push-Location -Path .\monkey_island\cc\ui
eslint ./src -c ./.eslintrc

Pop-Location
Pop-Location
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown');
deactivate
