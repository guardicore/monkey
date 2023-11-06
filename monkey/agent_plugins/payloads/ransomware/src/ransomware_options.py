from typing import Annotated, Optional

from monkeytypes import InfectionMonkeyBaseModel
from pydantic import Field, StringConstraints

valid_file_extension_pattern = r"^(\.[A-Za-z0-9_]+)?$"

_empty_pattern = "^$"

_linux_absolute_path_pattern = "^/"  # path starts with `/`
_linux_path_starts_with_env_variable_pattern = r"^\$"  # path starts with `$`
_linux_path_starts_with_tilde_pattern = "^~"  # path starts with `~`
valid_ransomware_path_linux_pattern = "|".join(
    [
        _empty_pattern,
        _linux_absolute_path_pattern,
        _linux_path_starts_with_env_variable_pattern,
        _linux_path_starts_with_tilde_pattern,
    ]
)


_windows_absolute_path_pattern = "^([A-Za-z]:(\\\\|/))"  # path starts like `C:\` OR `C:/`
_windows_env_var_non_numeric_pattern = r"[A-Za-z#$'()*+,\-\.?@\[\]_`\{\}~ ]"
_windows_path_starts_with_env_variable_pattern = rf"^%({_windows_env_var_non_numeric_pattern}+({_windows_env_var_non_numeric_pattern}|\d)*)%"  # noqa: E501  # path starts like `$` OR `%abc%`
_windows_unc_path_pattern = "^\\\\{2}"  # path starts like `\\`
valid_ransomware_path_windows_pattern = "|".join(
    [
        _empty_pattern,
        _windows_absolute_path_pattern,
        _windows_path_starts_with_env_variable_pattern,
        _windows_unc_path_pattern,
    ]
)


FileExtension = Annotated[str, StringConstraints(pattern=valid_file_extension_pattern)]
LinuxDirectory = Annotated[str, StringConstraints(pattern=valid_ransomware_path_linux_pattern)]
WindowsDirectory = Annotated[str, StringConstraints(pattern=valid_ransomware_path_windows_pattern)]


class RansomwareOptions(InfectionMonkeyBaseModel):
    file_extension: FileExtension = Field(
        default=".m0nk3y",
        description="The file extension that the Infection Monkey will use for the encrypted file.",
    )
    linux_target_dir: Optional[LinuxDirectory] = Field(
        default=None,
        description="A path to a directory on Linux systems that contains files you will allow "
        "Infection Monkey to encrypt. If no directory is specified, no files will be encrypted.",
    )
    windows_target_dir: Optional[WindowsDirectory] = Field(
        default=None,
        description="A path to a directory on Windows systems that contains files you will allow "
        "Infection Monkey to encrypt. If no directory is specified, no files will be encrypted.",
    )
    leave_readme: bool = Field(
        default=True,
        description="If enabled, Infection Monkey will leave a ransomware note in the target "
        "directory.",
    )
    change_wallpaper: bool = Field(
        default=True,
        description=(
            "If enabled, Infection Monkey will change the Desktop Wallpaper "
            "in Windows Systems, explaining that the computer was part of a "
            "Ransomware Simulation."
        ),
    )
