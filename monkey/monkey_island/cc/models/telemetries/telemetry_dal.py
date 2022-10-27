from __future__ import annotations

from typing import List

from monkey_island.cc.database import mongo


def get_telemetry_by_query(query: dict, output_fields=None) -> List[dict]:
    return mongo.db.telemetry.find(query, output_fields)
