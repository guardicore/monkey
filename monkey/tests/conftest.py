import pytest


@pytest.fixture(params=[".m0nk3y", ".test", ""], ids=["monkeyext", "testext", "noext"])
def ransomware_file_extension(request):
    return request.param
