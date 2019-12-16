REM - Runs MongoDB Server & Monkey Island Server using built pyinstaller EXE -
if not exist db mkdir db
start windows\run_mongodb.bat
start windows\run_cc_exe.bat
start https://localhost:5000