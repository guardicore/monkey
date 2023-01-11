import pytest

from infection_monkey.utils.monkey_log_path import (
    create_secure_agent_log_file,
    create_secure_dropper_log_file,
)


def delete_log_file(log_path):
    if log_path.is_file():
        log_path.unlink()


@pytest.mark.parametrize(
    "create_secure_log_file", [create_secure_agent_log_file, create_secure_dropper_log_file]
)
def test_subsequent_calls_return_same_path(create_secure_log_file):
    log_path_1 = create_secure_log_file()
    assert log_path_1.is_file()

    log_path_2 = create_secure_log_file()
    assert log_path_1 == log_path_2

    delete_log_file(log_path_1)


def test_agent_dropper_paths_differ():
    agent_log_path = create_secure_agent_log_file()
    dropper_log_path = create_secure_dropper_log_file()

    assert agent_log_path != dropper_log_path

    for log_path in [agent_log_path, dropper_log_path]:
        delete_log_file(log_path)
