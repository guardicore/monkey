from __future__ import annotations

from typing import List

from monkey_island.cc.database import mongo
from monkey_island.cc.models import CommandControlChannel
from monkey_island.cc.models.telemetries.telemetry import Telemetry


def save_telemetry(telemetry_dict: dict):
    cc_channel = CommandControlChannel(
        src=telemetry_dict["command_control_channel"]["src"],
        dst=telemetry_dict["command_control_channel"]["dst"],
    )
    Telemetry(
        data=telemetry_dict["data"],
        timestamp=telemetry_dict["timestamp"],
        monkey_guid=telemetry_dict["monkey_guid"],
        telem_category=telemetry_dict["telem_category"],
        command_control_channel=cc_channel,
    ).save()


def get_telemetry_by_query(query: dict, output_fields=None) -> List[dict]:
    return mongo.db.telemetry.find(query, output_fields)
