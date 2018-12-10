SET command=. .\deploy_windows.ps1; Deploy-Windows
if NOT "%~1" == "" ( 
    SET "command=%command% -monkey_home %~1"
)
if NOT "%~2" == "" ( 
    SET "command=%command% -branch %~2"
)
powershell -ExecutionPolicy ByPass -Command %command%