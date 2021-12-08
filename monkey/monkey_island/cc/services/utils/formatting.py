from datetime import datetime

from common.common_consts.time_formats import DEFAULT_TIME_FORMAT


def timestamp_to_date(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp).strftime(DEFAULT_TIME_FORMAT)
