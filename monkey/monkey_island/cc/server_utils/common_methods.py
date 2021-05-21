import platform

WINDOWS = "Windows"
LINUX = "Linux"


def get_runtime_os() -> str:
    if platform.system() == "Windows":
        return WINDOWS
    else:
        return LINUX
