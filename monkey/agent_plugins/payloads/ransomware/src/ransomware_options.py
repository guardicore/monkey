import re

from pydantic import Field, validator

from common.base_models import InfectionMonkeyBaseModel

valid_file_extension_regex = re.compile(r"^[\.(A-Za-z0-9_)+]*$")

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


class EncryptionBehavior(InfectionMonkeyBaseModel):
    file_extension: str = Field(
        default=".m0nk3y",
        description="The file extension that the Infection Monkey will use"
        " for the encrypted file.",
    )
    linux_target_dir: str = Field(
        default="",
        description="A path to a directory on Linux systems that contains"
        " files you will allow Infection Monkey to encrypt. If no"
        " directory is specified, no files will be encrypted.",
    )
    windows_target_dir: str = Field(
        default="",
        description="A path to a directory on Windows systems that contains"
        " files you will allow Infection Monkey to encrypt. If no"
        " directory is specified, no files will be encrypted.",
    )

    @validator("file_extension")
    def validate_file_extension(cls, file_extension):
        if not re.match(valid_file_extension_regex, file_extension):
            raise ValueError("Invalid file extension provided")
        return file_extension

    @validator("linux_target_dir")
    def validate_linux_target_dir(cls, linux_target_dir):
        if not re.match(valid_ransomware_path_linux_regex, linux_target_dir):
            raise ValueError("Invalid Linux target directory provided")
        return linux_target_dir

    @validator("windows_target_dir")
    def validate_windows_target_dir(cls, windows_target_dir):
        if not re.match(valid_ransomware_path_windows_regex, windows_target_dir):
            raise ValueError("Invalid Windows target directory provided")
        return windows_target_dir


class OtherBehaviors(InfectionMonkeyBaseModel):
    pass


class RansomwareOptions(InfectionMonkeyBaseModel):
    encryption: EncryptionBehavior = Field(
        title="Encrypt files",
        description="Ransomware encryption will be simulated by flipping every bit"
        " in the files contained within the target directories.",
        default=EncryptionBehavior(),
    )
    other_behaviors: OtherBehaviors = Field(default=OtherBehaviors())
