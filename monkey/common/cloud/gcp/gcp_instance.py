import logging

import requests

from common.cloud.environment_names import Environment
from common.cloud.instance import CloudInstance
from common.common_consts.timeouts import SHORT_REQUEST_TIMEOUT

logger = logging.getLogger(__name__)

GCP_METADATA_SERVICE_URL = "http://metadata.google.internal/"


class GcpInstance(CloudInstance):
    """
    Used to determine if on GCP. See https://cloud.google.com/compute/docs/storing-retrieving
    -metadata#runninggce
    """

    def is_instance(self):
        return self._on_gcp

    def get_cloud_provider_name(self) -> Environment:
        return Environment.GCP

    def __init__(self):
        self._on_gcp = False

        try:
            # If not on GCP, this domain shouldn't resolve.
            response = requests.get(GCP_METADATA_SERVICE_URL, timeout=SHORT_REQUEST_TIMEOUT)

            if response:
                logger.debug("Got ok metadata response: on GCP")
                self._on_gcp = True

                if "Metadata-Flavor" not in response.headers:
                    logger.warning("Got unexpected GCP Metadata format")
                else:
                    if not response.headers["Metadata-Flavor"] == "Google":
                        logger.warning(
                            "Got unexpected Metadata flavor: {}".format(
                                response.headers["Metadata-Flavor"]
                            )
                        )
            else:
                logger.warning(
                    "On GCP, but metadata response not ok: {}".format(response.status_code)
                )
        except requests.RequestException:
            logger.debug(
                "Failed to get response from GCP metadata service: This instance is not on GCP"
            )
            self._on_gcp = False
