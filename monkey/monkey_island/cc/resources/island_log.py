import logging
from pathlib import Path

from common.utils.file_utils import get_text_file_contents
from monkey_island.cc.resources.AbstractResource import AbstractResource

logger = logging.getLogger(__name__)


class IslandLog(AbstractResource):
    urls = ["/api/island/log"]

    def __init__(self, island_log_file_path: Path):
        self._island_log_file_path = island_log_file_path

    def get(self):
        try:
            return get_text_file_contents(self._island_log_file_path)
        except Exception:
            logger.error("Monkey Island logs failed to download", exc_info=True)
