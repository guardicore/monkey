import os

import pytest

from monkey_island.cc.setup.mongo_process_runner import MongoDbRunner

TEST_DIR_NAME = "test_dir"


@pytest.fixture(autouse=True)
def fake_db_dir(monkeypatch, tmpdir):
    monkeypatch.setattr("monkey_island.cc.setup.mongo_process_runner.DB_DIR_NAME", TEST_DIR_NAME)


@pytest.fixture
def expected_path(monkeypatch, tmpdir):
    expected_path = os.path.join(tmpdir, TEST_DIR_NAME)
    return expected_path


def test_create_db_dir(monkeypatch, tmpdir, expected_path):
    db_path = MongoDbRunner(tmpdir, tmpdir)._create_db_dir()
    assert os.path.isdir(expected_path)
    assert db_path == expected_path


def test_create_db_dir__already_created(monkeypatch, tmpdir, expected_path):
    os.mkdir(expected_path)

    db_path = MongoDbRunner(tmpdir, tmpdir)._create_db_dir()
    assert os.path.isdir(expected_path)
    assert db_path == expected_path
