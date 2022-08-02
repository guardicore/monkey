import logging
from pathlib import Path

from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.request_authentication import jwt_required
from monkey_island.cc.server_utils.island_logger import get_log_file_contents

logger = logging.getLogger(__name__)


class IslandLog(AbstractResource):
    urls = ["/api/island/log"]

    def __init__(self, island_log_file_path: Path):
        self._island_log_file_path = island_log_file_path

    @jwt_required
    def get(self):
        try:
            return get_log_file_contents(self._island_log_file_path)
        except Exception:
            logger.error("Monkey Island logs failed to download", exc_info=True)
