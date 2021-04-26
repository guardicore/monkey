REM - Runs MongoDB Server & Monkey Island Server using python -
if not exist db mkdir db
start windows\run_mongodb.bat
pipenv run windows\run_cc.bat
start https://localhost:5000
