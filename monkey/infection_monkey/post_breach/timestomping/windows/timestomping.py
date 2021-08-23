from pathlib import Path

TIMESTOMPING_SCRIPT = Path(__file__).parent / "timestomping.ps1"


def get_windows_timestomping_commands():
    return f"powershell.exe {TIMESTOMPING_SCRIPT}"


# Commands' source: https://github.com/redcanaryco/atomic-red-team/blob/master/atomics/T1070.006
# /T1070.006.md
