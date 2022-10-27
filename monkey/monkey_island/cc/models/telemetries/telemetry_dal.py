from __future__ import annotations

from typing import List

from monkey_island.cc.database import mongo
from monkey_island.cc.models.telemetries.telemetry import Telemetry


def save_telemetry(telemetry_dict: dict):
    Telemetry(
        data=telemetry_dict["data"],
        timestamp=telemetry_dict["timestamp"],
        monkey_guid=telemetry_dict["monkey_guid"],
        telem_category=telemetry_dict["telem_category"],
    ).save()


def get_telemetry_by_query(query: dict, output_fields=None) -> List[dict]:
    return mongo.db.telemetry.find(query, output_fields)
