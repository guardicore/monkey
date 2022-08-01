import re
from pathlib import PureWindowsPath

from marshmallow import ValidationError

valid_windows_custom_pba_filename_regex = re.compile(r"^[^<>:\"\\\/|?*]*[^<>:\"\\\/|?* \.]+$|^$")
valid_linux_custom_pba_filename_regex = re.compile(r"^[^\0/]*$")


def validate_windows_custom_pba_filename(windows_filename: str):
    validate_windows_filename_not_reserved(windows_filename)
    if not re.match(valid_windows_custom_pba_filename_regex, windows_filename):
        raise ValidationError(f"Invalid Windows filename {windows_filename}: illegal characters")


def validate_windows_filename_not_reserved(windows_filename: str):
    # filename shouldn't start with any of these and be followed by a period
    if PureWindowsPath(windows_filename).is_reserved():
        raise ValidationError(f"Invalid Windows filename {windows_filename}: reserved name used")
