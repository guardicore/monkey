import pytest


@pytest.fixture
def patched_home_env(monkeypatch, tmpdir):
    monkeypatch.setenv("HOME", str(tmpdir))

    return tmpdir
