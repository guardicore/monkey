import pytest

from infection_monkey.utils.monkey_log_path import get_agent_log_path, get_dropper_log_path


def delete_log_file(log_path):
    if log_path.is_file():
        log_path.unlink()


@pytest.mark.parametrize("get_log_path", [get_agent_log_path, get_dropper_log_path])
def test_subsequent_calls_return_same_path(get_log_path):
    log_path_1 = get_log_path()
    assert log_path_1.is_file()

    log_path_2 = get_log_path()
    assert log_path_1 == log_path_2

    delete_log_file(log_path_1)


def test_agent_dropper_paths_differ():
    agent_log_path = get_agent_log_path()
    dropper_log_path = get_dropper_log_path()

    assert agent_log_path != dropper_log_path

    for log_path in [agent_log_path, dropper_log_path]:
        delete_log_file(log_path)
