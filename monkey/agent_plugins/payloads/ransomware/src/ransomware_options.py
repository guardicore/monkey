import re
from typing import Optional

from pydantic import ConstrainedStr, Field

from common.base_models import InfectionMonkeyBaseModel

valid_file_extension_regex = re.compile(r"^(\.[A-Za-z0-9_]+)?$")

_empty_regex = re.compile("^$")

_linux_absolute_path_regex = re.compile("^/")  # path starts with `/`
_linux_path_starts_with_env_variable_regex = re.compile(r"^\$")  # path starts with `$`
_linux_path_starts_with_tilde_regex = re.compile("^~")  # path starts with `~`
valid_ransomware_path_linux_regex = re.compile(
    "|".join(
        [
            _empty_regex.pattern,
            _linux_absolute_path_regex.pattern,
            _linux_path_starts_with_env_variable_regex.pattern,
            _linux_path_starts_with_tilde_regex.pattern,
        ]
    )
)

_windows_absolute_path_regex = re.compile("^([A-Za-z]:(\\\\|/))")  # path starts like `C:\` OR `C:/`
_windows_env_var_non_numeric_regex = re.compile(r"[A-Za-z#$'()*+,\-\.?@[\]_`\{\}~ ]")
_windows_path_starts_with_env_variable_regex = re.compile(
    rf"^%({_windows_env_var_non_numeric_regex.pattern}+({_windows_env_var_non_numeric_regex.pattern}|\d)*)%"  # noqa: E501
)  # path starts like `$` OR `%abc%`
_windows_unc_path_regex = re.compile("^\\\\{2}")  # path starts like `\\`
valid_ransomware_path_windows_regex = re.compile(
    "|".join(
        [
            _empty_regex.pattern,
            _windows_absolute_path_regex.pattern,
            _windows_path_starts_with_env_variable_regex.pattern,
            _windows_unc_path_regex.pattern,
        ]
    )
)


class FileExtension(ConstrainedStr):
    regex = valid_file_extension_regex


class LinuxDirectory(ConstrainedStr):
    regex = valid_ransomware_path_linux_regex


class WindowsDirectory(ConstrainedStr):
    regex = valid_ransomware_path_windows_regex


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
