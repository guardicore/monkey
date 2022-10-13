from typing import Any, Dict

from monkey_island.cc.models import Machine


def fixup_group_and_os(formatted_node: Dict[str, Any], machine: Machine) -> Dict[str, Any]:
    if not machine.operating_system:
        return formatted_node
    if "unknown" in formatted_node["group"]:
        formatted_node["group"] = formatted_node["group"].replace(
            "unknown", machine.operating_system.value
        )
    if "unknown" in formatted_node["os"]:
        formatted_node["os"] = formatted_node["os"] = machine.operating_system.value
    return formatted_node
