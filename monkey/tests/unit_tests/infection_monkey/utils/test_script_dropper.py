from pathlib import PurePosixPath

from infection_monkey.utils import build_bash_dropper


def test_build_bash_dropper():
    agent_dst_path = PurePosixPath("/tmp/agent")
    run_command = f"env=some_value {agent_dst_path} --monkey-id 1234 --monkey-name test-monkey 42"
    agent_binary_line_1 = b"hello"
    agent_binary_line_2 = b"world"
    agent_binary = agent_binary_line_1 + b"\n" + agent_binary_line_2

    bash_dropper = build_bash_dropper(agent_dst_path, run_command, agent_binary)
    bash_dropper_lines = bash_dropper.split(b"\n")

    assert bash_dropper_lines[-2] == agent_binary_line_1
    assert bash_dropper_lines[-1] == agent_binary_line_2
    assert run_command.encode() in bash_dropper
