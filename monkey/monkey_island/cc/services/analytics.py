import logging

import requests

from monkey_island.cc import Version
from monkey_island.cc.deployment import Deployment

logger = logging.getLogger(__name__)

ANALYTICS_URL = (
    "https://m15mjynko3.execute-api.us-east-1.amazonaws.com/default?version={"
    "version}&deployment={deployment}"
)


class Analytics:
    def __init__(self, version: Version, deployment: Deployment):
        self.version = version.version_number
        self.deployment = deployment.value
        self._send_analytics()

    def _send_analytics(self):
        url = ANALYTICS_URL.format(deployment=self.deployment, version=self.version)
        response = requests.get(url).json()
        logger.info(
            f"Version number and deployment type was sent to analytics server."
            f" The response is: {response}"
        )
