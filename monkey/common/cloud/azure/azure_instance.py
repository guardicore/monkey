import logging

import requests

from common.cloud.environment_names import Environment
from common.cloud.instance import CloudInstance

LATEST_AZURE_METADATA_API_VERSION = "2019-04-30"
AZURE_METADATA_SERVICE_URL = "http://169.254.169.254/metadata/instance?api-version=%s" % LATEST_AZURE_METADATA_API_VERSION

logger = logging.getLogger(__name__)


class AzureInstance(CloudInstance):
    """
    Access to useful information about the current machine if it's an Azure VM.
    Based on Azure metadata service: https://docs.microsoft.com/en-us/azure/virtual-machines/windows/instance-metadata-service
    """
    def is_instance(self):
        return self.on_azure

    def get_cloud_provider_name(self) -> Environment:
        return Environment.AZURE

    def __init__(self):
        """
        Determines if on Azure and if so, gets some basic metadata on this instance.
        """
        self.instance_name = None
        self.instance_id = None
        self.location = None
        self.on_azure = False

        try:
            response = requests.get(AZURE_METADATA_SERVICE_URL, headers={"Metadata": "true"})
            self.on_azure = True

            # If not on cloud, the metadata URL is non-routable and the connection will fail.
            # If on AWS, should get 404 since the metadata service URL is different, so bool(response) will be false.
            if response:
                logger.debug("On Azure. Trying to parse metadata.")
                self.try_parse_response(response)
            else:
                logger.warning("On Azure, but metadata response not ok: {}".format(response.status_code))
        except requests.RequestException:
            logger.debug("Failed to get response from Azure metadata service: This instance is not on Azure.")
            self.on_azure = False

    def try_parse_response(self, response):
        try:
            response_data = response.json()
            self.instance_name = response_data["compute"]["name"]
            self.instance_id = response_data["compute"]["vmId"]
            self.location = response_data["compute"]["location"]
        except KeyError:
            logger.exception("Error while parsing response from Azure metadata service.")
