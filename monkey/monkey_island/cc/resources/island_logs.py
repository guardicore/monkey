import logging
from pathlib import Path

from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.request_authentication import jwt_required

logger = logging.getLogger(__name__)


class IslandLog(AbstractResource):
    urls = ["/api/island/log"]

    def __init__(self, island_log_file_path: Path):
        self._island_log_file_path = island_log_file_path

    @jwt_required
    def get(self):
        try:
            return self._get_log_file_contents()
        except Exception:
            logger.error("Monkey Island logs failed to download", exc_info=True)

    def _get_log_file_contents(self):
        with open(self._island_log_file_path, "rt") as f:
            log_file = f.read()
        return {"log_file": log_file}
