import os
import pwd
from pathlib import Path

import pytest

from infection_monkey.credential_collectors import SSHKeypair, Username
from infection_monkey.credential_collectors.ssh_collector import SSHCollector


@pytest.fixture
def project_name(pytestconfig):
    home_dir = str(Path.home())
    return "/" / Path(str(pytestconfig.rootdir).replace(home_dir, ""))


@pytest.fixture
def ssh_test_dir(project_name):
    return project_name / "monkey" / "tests" / "data_for_tests" / "ssh_info"


@pytest.fixture
def get_username():
    return pwd.getpwuid(os.getuid()).pw_name


@pytest.mark.skipif(os.name != "posix", reason="We run SSH only on Linux.")
def test_ssh_credentials_collector_success(ssh_test_dir, get_username, monkeypatch):
    monkeypatch.setattr(
        "infection_monkey.credential_collectors.ssh_collector.SSHCollector.default_dirs",
        [str(ssh_test_dir / "ssh_info_full")],
    )

    ssh_credentials = SSHCollector().collect_credentials()

    assert len(ssh_credentials.identities) == 1
    assert type(ssh_credentials.identities[0]) == Username
    assert "username" in ssh_credentials.identities[0].content
    assert ssh_credentials.identities[0].content["username"] == get_username

    assert len(ssh_credentials.secrets) == 1
    assert type(ssh_credentials.secrets[0]) == SSHKeypair

    assert len(ssh_credentials.secrets[0].content) == 3
    assert (
        ssh_credentials.secrets[0]
        .content["private_key"]
        .startswith("-----BEGIN OPENSSH PRIVATE KEY-----")
    )
    assert (
        ssh_credentials.secrets[0]
        .content["public_key"]
        .startswith("ssh-ed25519 something-public-here")
    )
    assert ssh_credentials.secrets[0].content["known_hosts"].startswith("|1|really+known+host")


@pytest.mark.skipif(os.name != "posix", reason="We run SSH only on Linux.")
def test_no_ssh_credentials(monkeypatch):
    monkeypatch.setattr(
        "infection_monkey.credential_collectors.ssh_collector.SSHCollector.default_dirs", []
    )

    ssh_credentials = SSHCollector().collect_credentials()

    assert len(ssh_credentials.identities) == 0
    assert len(ssh_credentials.secrets) == 0


@pytest.mark.skipif(os.name != "posix", reason="We run SSH only on Linux.")
def test_ssh_collector_partial_credentials(monkeypatch, ssh_test_dir):
    monkeypatch.setattr(
        "infection_monkey.credential_collectors.ssh_collector.SSHCollector.default_dirs",
        [str(ssh_test_dir / "ssh_info_partial")],
    )

    ssh_credentials = SSHCollector().collect_credentials()

    assert len(ssh_credentials.secrets[0].content) == 3
    assert ssh_credentials.secrets[0].content["private_key"] is None
    assert ssh_credentials.secrets[0].content["known_hosts"] is None


@pytest.mark.skipif(os.name != "posix", reason="We run SSH only on Linux.")
def test_ssh_collector_no_public_key(monkeypatch, ssh_test_dir):
    monkeypatch.setattr(
        "infection_monkey.credential_collectors.ssh_collector.SSHCollector.default_dirs",
        [str(ssh_test_dir / "ssh_info_no_public_key")],
    )

    ssh_credentials = SSHCollector().collect_credentials()

    assert len(ssh_credentials.identities) == 0
    assert len(ssh_credentials.secrets) == 0
