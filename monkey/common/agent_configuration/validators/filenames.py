import re
from pathlib import PureWindowsPath

from marshmallow import ValidationError

_valid_windows_filename_regex = re.compile(r"^[^<>:\"\\\/|?*]*[^<>:\"\\\/|?* \.]+$|^$")
_valid_linux_filename_regex = re.compile(r"^[^\0/]*$")


def validate_linux_filename(linux_filename: str):
    if not re.match(_valid_linux_filename_regex, linux_filename):
        raise ValidationError(f"Invalid Unix filename {linux_filename}: illegal characters")


def validate_windows_filename(windows_filename: str):
    _validate_windows_filename_not_reserved(windows_filename)
    if not re.match(_valid_windows_filename_regex, windows_filename):
        raise ValidationError(f"Invalid Windows filename {windows_filename}: illegal characters")


def _validate_windows_filename_not_reserved(windows_filename: str):
    # filename shouldn't start with any of these and be followed by a period
    if PureWindowsPath(windows_filename).is_reserved():
        raise ValidationError(f"Invalid Windows filename {windows_filename}: reserved name used")
