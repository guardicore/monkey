import pytest


@pytest.fixture
def patched_home_env(monkeypatch, tmp_path):
    monkeypatch.setenv("HOME", str(tmp_path))

    return tmp_path
