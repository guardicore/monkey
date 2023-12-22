from unittest.mock import MagicMock

import pytest
from agent_plugins.payloads.ransomware.src.wallpaper_changer import WallpaperChanger
from monkeytypes import OperatingSystem


@pytest.fixture
def SystemParametersInfoW() -> MagicMock:
    return MagicMock()


@pytest.fixture
def ctypes(SystemParametersInfoW: MagicMock) -> MagicMock:
    ctypes = MagicMock()
    ctypes.windll = MagicMock()
    ctypes.windll.user32 = MagicMock()
    ctypes.windll.user32.SystemParametersInfoW = SystemParametersInfoW

    return ctypes


@pytest.fixture(autouse=True)
def patch_ctypes(monkeypatch, ctypes):
    monkeypatch.setattr("agent_plugins.payloads.ransomware.src.wallpaper_changer.ctypes", ctypes)


def test_windows(SystemParametersInfoW: MagicMock):
    wallpaper_changer = WallpaperChanger(OperatingSystem.WINDOWS)

    wallpaper_changer.change_wallpaper()

    assert SystemParametersInfoW.call_count == 1


def test_not_windows(SystemParametersInfoW: MagicMock):
    wallpaper_changer = WallpaperChanger(OperatingSystem.LINUX)

    with pytest.raises(NotImplementedError):
        wallpaper_changer.change_wallpaper()

    assert SystemParametersInfoW.call_count == 0
