from PyInstaller.utils.hooks import collect_data_files, collect_submodules

hiddenimports = collect_submodules('infection_monkey.network')
datas = (collect_data_files('infection_monkey.network', include_py_files=True))
