pyinstaller -F --log-level=DEBUG --clean --upx-dir=.\bin monkey_island.spec
move dist\monkey_island.exe monkey_island.exe
rmdir /S /Q build
rmdir /S /Q dist
