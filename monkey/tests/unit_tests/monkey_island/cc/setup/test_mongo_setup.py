import os

from monkey_island.cc.setup.mongo_setup import _create_db_dir


def test_create_db_dir(monkeypatch, tmpdir):
    test_dir_name = "test_dir"
    monkeypatch.setattr("monkey_island.cc.setup.mongo_setup.DB_DIR_NAME", test_dir_name)
    expected_path = os.path.join(tmpdir, test_dir_name)

    db_path = _create_db_dir(tmpdir)
    assert os.path.isdir(expected_path)
    assert db_path == expected_path


def test_create_db_dir_already_created(monkeypatch, tmpdir):
    test_dir_name = "test_dir"
    monkeypatch.setattr("monkey_island.cc.setup.mongo_setup.DB_DIR_NAME", test_dir_name)
    expected_path = os.path.join(tmpdir, test_dir_name)
    os.mkdir(expected_path)

    db_path = _create_db_dir(tmpdir)
    assert os.path.isdir(expected_path)
    assert db_path == expected_path
