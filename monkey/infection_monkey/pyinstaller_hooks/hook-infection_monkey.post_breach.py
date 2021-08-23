from PyInstaller.utils.hooks import collect_data_files

datas = collect_data_files("infection_monkey.post_breach", include_py_files=False)
