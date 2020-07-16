from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Import all actions as modules
hiddenimports = collect_submodules('infection_monkey.system_info.collectors')
# Add action files that we enumerate
datas = (collect_data_files('infection_monkey.system_info.collectors', include_py_files=True))
