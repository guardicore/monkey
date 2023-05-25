import pytest

from common.types import FileExtension


@pytest.mark.parametrize(
    "invalid_extension",
    [
        "testext",
        "testext.",
        ".te\\stext",
        ".testext/",
        ".test/ext",
        "\\.testext",
        "/.testext",
        "./testext",
        ".\\testext",
        "",
    ],
)
def test_invalid_file_extension(invalid_extension: str):
    with pytest.raises(ValueError):
        FileExtension(invalid_extension)


@pytest.mark.parametrize(
    "valid_extension", [".testext", ".m0nk3y", ".cryptowall", ".st!uff", ".encrypted"]
)
def test_valid_file_extension(valid_extension: str):
    fe = FileExtension(valid_extension)

    assert fe == valid_extension
