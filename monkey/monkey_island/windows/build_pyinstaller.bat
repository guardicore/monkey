pyinstaller -F --log-level=DEBUG --clean --upx-dir=.\bin monkey_island.spec
move /Y dist\monkey_island.exe monkey_island.exe
IF EXIST build (
	rmdir /S /Q build
)
IF EXIST dist (
	rmdir /S /Q dist
)