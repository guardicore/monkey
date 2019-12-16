from PyInstaller.utils.hooks import collect_submodules, collect_data_files

# Import all actions as modules
hiddenimports = collect_submodules('infection_monkey.post_breach.actions')
# Add action files that we enumerate
datas = (collect_data_files('infection_monkey.post_breach.actions', include_py_files=True))
