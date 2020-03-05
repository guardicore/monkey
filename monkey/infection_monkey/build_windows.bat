REM Check if build ID was passed to the build script.
if "%1"=="" GOTO START_BUILD

REM Validate build ID
echo %1|findstr /r "^[0-9a-zA-Z]*$"
if %errorlevel% neq 0 (exit /b %errorlevel%)

REM replace build ID
echo %1> ../common/BUILD

:START_BUILD
pyinstaller -F --log-level=DEBUG --clean --upx-dir=.\bin monkey.spec
