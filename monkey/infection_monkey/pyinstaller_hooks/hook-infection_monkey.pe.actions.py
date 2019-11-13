from PyInstaller.utils.hooks import collect_submodules, collect_data_files

# Import all exploiters as modules
hiddenimports = collect_submodules('infection_monkey.privilege_escalation.exploiters')
# Add action files that we enumerate
datas = (collect_data_files('infection_monkey.privilege_escalation.exploiters', include_py_files=True))
