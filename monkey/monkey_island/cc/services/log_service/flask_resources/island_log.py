import logging
from http import HTTPStatus
from pathlib import Path

from flask_security import auth_token_required, roles_accepted
from monkeytoolbox import get_text_file_contents

from monkey_island.cc.flask_utils import AbstractResource
from monkey_island.cc.services.authentication_service import AccountRole

logger = logging.getLogger(__name__)


class IslandLog(AbstractResource):
    urls = ["/api/island/log"]

    def __init__(self, island_log_file_path: Path):
        self._island_log_file_path = island_log_file_path

    @auth_token_required
    @roles_accepted(AccountRole.ISLAND_INTERFACE.name)
    def get(self):
        try:
            return get_text_file_contents(self._island_log_file_path)
        except FileNotFoundError:
            logger.error("Monkey Island logs do not exist", exc_info=True)
            return "", HTTPStatus.NOT_FOUND
        except Exception:
            logger.error("Monkey Island logs failed to download", exc_info=True)
