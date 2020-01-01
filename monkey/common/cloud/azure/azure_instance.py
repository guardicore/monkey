import requests

AZURE_METADATA_SERVICE_URL = "http://169.254.169.254/metadata/instance?api-version=2019-06-04"


class AzureInstance(object):
    """
    Access to useful information about the current machine if it's an Azure VM.
    """

    def __init__(self):
        try:
            response = requests.get(AZURE_METADATA_SERVICE_URL, headers={"Metadata": "true"})
            if response:
                self.on_azure = True
                self.try_parse_response(response)
            else:
                self.on_azure = False
        except ConnectionError:
            self.on_azure = False

    def try_parse_response(self, response):
        # TODO implement - get fields from metadata like region etc.
        pass

    def is_azure_instance(self):
        return self.on_azure
