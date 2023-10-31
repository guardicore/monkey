import threading
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from monkeytypes import AgentID, Credentials, SSHKeypair, Username

from common.event_queue import IAgentEventPublisher

pwd = pytest.importorskip("pwd")
# we need to check if `pwd` can be imported before importing `Plugin`
from agent_plugins.credentials_collectors.ssh.src.plugin import Plugin  # noqa: E402

AGENT_ID = AgentID("ed077054-a316-479a-a99d-75bb378c0a6e")


@pytest.fixture
def mock_agent_event_publisher() -> IAgentEventPublisher:
    return MagicMock(spec=IAgentEventPublisher)


def test_pwd_exception(monkeypatch, mock_agent_event_publisher: IAgentEventPublisher):
    mock_pwd = MagicMock()
    mock_pwd.getpwall = MagicMock(side_effect=Exception)
    monkeypatch.setattr("agent_plugins.credentials_collectors.ssh.src.plugin.pwd", mock_pwd)

    stolen_credentials = Plugin(
        agent_id=AGENT_ID, agent_event_publisher=mock_agent_event_publisher
    ).run(options={}, interrupt=threading.Event())

    assert len(stolen_credentials) == 0
    assert mock_agent_event_publisher.publish.call_count == 0  # type: ignore[attr-defined]


USERNAME_1 = "test_user_1"
PUBLIC_KEY_1a = "pubkey1a"
PRIVATE_KEY_1a = "-----BEGIN DSA PRIVATE privkey1a"
PRIVATE_KEY_1b = "-----BEGIN ECDSA PRIVATE privkey1b"

IDENTITY_1 = Username(username=USERNAME_1)
SECRET_1a = SSHKeypair(private_key=PRIVATE_KEY_1a, public_key=PUBLIC_KEY_1a)
SECRET_1b = SSHKeypair(private_key=PRIVATE_KEY_1b, public_key=None)

USERNAME_2 = "test_user_2"
PRIVATE_KEY_2 = "-----BEGIN EC PRIVATE privkey2"

IDENTITY_2 = Username(username=USERNAME_2)
SECRET_2 = SSHKeypair(private_key=PRIVATE_KEY_2, public_key=None)

CREDENTIALS = {
    Credentials(identity=IDENTITY_1, secret=SECRET_1a),
    Credentials(identity=IDENTITY_1, secret=SECRET_1b),
    Credentials(identity=IDENTITY_2, secret=SECRET_2),
}


@pytest.fixture
def place_key_files(tmp_path):
    inaccessible_root_ssh_dir = tmp_path / "root/.ssh"
    inaccessible_root_ssh_dir.mkdir(parents=True)
    inaccessible_root_ssh_dir.chmod(mode=0o200)

    inaccessible_home_dir = tmp_path / "daemon_home"
    inaccessible_home_dir.mkdir()
    (inaccessible_home_dir / ".ssh").mkdir()
    inaccessible_home_dir.chmod(0o000)

    user_1_ssh_dir = tmp_path / "home" / USERNAME_1 / ".ssh"
    user_1_ssh_dir.mkdir(parents=True)

    (user_1_ssh_dir / "key1").write_text(PRIVATE_KEY_1a)
    (user_1_ssh_dir / "key1.pub").write_text(PUBLIC_KEY_1a)
    (user_1_ssh_dir / "key2").write_text(PRIVATE_KEY_1b)

    (user_1_ssh_dir / "key2.pub").touch(mode=0o200)
    (user_1_ssh_dir / "unreadable").touch(mode=0o200)

    user_2_ssh_dir = tmp_path / "var/home" / USERNAME_2 / ".ssh"
    user_2_ssh_dir.mkdir(parents=True)

    (user_2_ssh_dir / "key2").write_text(PRIVATE_KEY_2)

    yield

    # Set these permissions so that pytest can clean up the directory
    inaccessible_root_ssh_dir.chmod(0o700)
    inaccessible_home_dir.chmod(0o700)


@pytest.fixture
def patch_pwd_getpwall(monkeypatch, place_key_files, tmp_path: Path):
    pwd_structs = [
        pwd.struct_passwd(  # type: ignore[attr-defined]
            [
                "root",
                "x",
                0,
                0,
                "root",
                tmp_path / "root",
                "/bin/bash",
            ]
        ),
        pwd.struct_passwd(  # type: ignore[attr-defined]
            [
                USERNAME_1,
                "x",
                4,
                65534,
                "sync",
                tmp_path / f"home/{USERNAME_1}",
                "/bin/sync",
            ]
        ),
        pwd.struct_passwd(  # type: ignore[attr-defined]
            [
                "daemon",
                "x",
                1,
                1,
                "daemon",
                tmp_path / "daemon_home",
                "/usr/sbin/nologin",
            ]
        ),
        pwd.struct_passwd(  # type: ignore[attr-defined]
            [
                USERNAME_2,
                "x",
                4,
                65534,
                "sync",
                tmp_path / f"var/home/{USERNAME_2}",
                "/bin/sync",
            ]
        ),
    ]
    mock_pwd = MagicMock()
    mock_pwd.getpwall = MagicMock(return_value=pwd_structs)
    monkeypatch.setattr("agent_plugins.credentials_collectors.ssh.src.plugin.pwd", mock_pwd)


def test_stolen_credentials(patch_pwd_getpwall, mock_agent_event_publisher):
    plugin = Plugin(agent_id=AGENT_ID, agent_event_publisher=mock_agent_event_publisher)
    stolen_credentials = plugin.run(options={}, interrupt=threading.Event())

    assert set(stolen_credentials) == CREDENTIALS
    assert mock_agent_event_publisher.publish.call_count == 1
    assert set(mock_agent_event_publisher.publish.call_args[0][0].stolen_credentials) == CREDENTIALS
