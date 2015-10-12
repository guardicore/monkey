@Echo Off
Set _Delay=10
Set _Monitor=Z:\
Set _Base=%temp%\BaselineState.dir
Set _Chck=%temp%\ChkState.dir
Set _OS=6
Set _SourceStore=C:\Code\monkey\chaos_monkey
Set _OutputName=%1
Set _BinariesOut=X:\
If "%_OutputName%"=="" Exit
Ver|Findstr /I /C:"Version 5">Nul
If %Errorlevel%==0 Set _OS=5
Echo Starting source monitor, output is %_OutputName%
:_StartMon
Call :_SetBaseline "%_Base%" "%_Monitor%"
:_MonLoop
If %_OS%==5 (Ping 127.0.0.1 -n 1 %_Delay%>Nul) Else Timeout %_Delay%>Nul
Call :_SetBaseline "%_Chck%" "%_Monitor%"
FC /A /L "%_Base%" "%_Chck%">Nul
If %ErrorLevel%==0 Goto _MonLoop
Echo Change Detected, Compiling...
rmdir /s /q "%_SourceStore%"
mkdir "%_SourceStore%"
xcopy /s /q "%_Monitor%" "%_SourceStore%"
pushd "%_SourceStore%"
cmd /c build_windows.bat
copy /y "dist\monkey.exe" "%_BinariesOut%%_OutputName%"
popd
echo Waiting for changes...
Goto :_StartMon
:::::::::::::::::::::::::::::::::::::::::::::::::::
:: Subroutine
:::::::::::::::::::::::::::::::::::::::::::::::::::
:_SetBaseline
If Exist "%temp%\tempfmstate.dir" Del "%temp%\tempfmstate.dir"
For /F "Tokens=* Delims=" %%I In ('Dir /S "%~2"') Do (
Set _Last=%%I
>>"%temp%\tempfmstate.dir" Echo.%%I
)
>"%~1" Findstr /V /C:"%_Last%" "%temp%\tempfmstate.dir"
Goto :EOF