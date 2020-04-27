from PyInstaller.utils.hooks import collect_submodules, collect_data_files

hiddenimports = collect_submodules('infection_monkey.network')
datas = (collect_data_files('infection_monkey.network', include_py_files=True))
