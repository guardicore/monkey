import logging

import requests
import simplejson

from common.cloud.environment_names import Environment
from common.cloud.instance import CloudInstance
from common.common_consts.timeouts import SHORT_REQUEST_TIMEOUT

LATEST_AZURE_METADATA_API_VERSION = "2019-04-30"
AZURE_METADATA_SERVICE_URL = "http://169.254.169.254/metadata/instance?api-version=%s" % LATEST_AZURE_METADATA_API_VERSION

logger = logging.getLogger(__name__)


class AzureInstance(CloudInstance):
    """
    Access to useful information about the current machine if it's an Azure VM.
    Based on Azure metadata service: https://docs.microsoft.com/en-us/azure/virtual-machines/windows/instance-metadata-service
    """
    def is_instance(self):
        return self._on_azure

    def get_cloud_provider_name(self) -> Environment:
        return Environment.AZURE

    def __init__(self):
        """
        Determines if on Azure and if so, gets some basic metadata on this instance.
        """
        self.instance_name = None
        self.instance_id = None
        self.location = None
        self._on_azure = False

        try:
            response = requests.get(AZURE_METADATA_SERVICE_URL,
                                    headers={"Metadata": "true"},
                                    timeout=SHORT_REQUEST_TIMEOUT)

            # If not on cloud, the metadata URL is non-routable and the connection will fail.
            # If on AWS, should get 404 since the metadata service URL is different, so bool(response) will be false.
            if response:
                logger.debug("Trying to parse Azure metadata.")
                self.try_parse_response(response)
            else:
                logger.warning(f"Metadata response not ok: {response.status_code}")
        except requests.RequestException:
            logger.debug("Failed to get response from Azure metadata service: This instance is not on Azure.")

    def try_parse_response(self, response):
        try:
            response_data = response.json()
            self.instance_name = response_data["compute"]["name"]
            self.instance_id = response_data["compute"]["vmId"]
            self.location = response_data["compute"]["location"]
            self._on_azure = True
        except (KeyError, simplejson.errors.JSONDecodeError) as e:
            logger.exception(f"Error while parsing response from Azure metadata service: {e}")
