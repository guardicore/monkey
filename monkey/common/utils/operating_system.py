import platform


def is_windows_os() -> bool:
    return platform.system() == "Windows"
