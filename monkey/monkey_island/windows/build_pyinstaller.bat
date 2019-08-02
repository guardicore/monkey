REM - Builds Monkey Island Server EXE using pyinstaller -
bin\Python27\Scripts\pyinstaller.exe -F --log-level=DEBUG --clean --upx-dir=.\bin monkey_island.spec
move /Y dist\monkey_island.exe monkey_island.exe
rmdir /S /Q build
rmdir /S /Q dist