import os

from monkey_island.cc.setup.mongo_process_runner import MongoDbRunner


def test_create_db_dir(monkeypatch, tmpdir):
    test_dir_name = "test_dir"
    monkeypatch.setattr("monkey_island.cc.setup.mongo_process_runner.DB_DIR_NAME", test_dir_name)
    expected_path = os.path.join(tmpdir, test_dir_name)

    db_path = MongoDbRunner(tmpdir, tmpdir)._create_db_dir()
    assert os.path.isdir(expected_path)
    assert db_path == expected_path


def test_create_db_dir__already_created(monkeypatch, tmpdir):
    test_dir_name = "test_dir"
    monkeypatch.setattr("monkey_island.cc.setup.mongo_process_runner.DB_DIR_NAME", test_dir_name)
    expected_path = os.path.join(tmpdir, test_dir_name)
    os.mkdir(expected_path)

    db_path = MongoDbRunner(tmpdir, tmpdir)._create_db_dir()
    assert os.path.isdir(expected_path)
    assert db_path == expected_path
