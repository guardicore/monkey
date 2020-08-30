import json
import logging
import re
import urllib.error
import urllib.request

from common.cloud.environment_names import Environment
from common.cloud.instance import CloudInstance

__author__ = 'itay.mizeretz'


AWS_INSTANCE_METADATA_LOCAL_IP_ADDRESS = "169.254.169.254"
AWS_LATEST_METADATA_URI_PREFIX = 'http://{0}/latest/'.format(AWS_INSTANCE_METADATA_LOCAL_IP_ADDRESS)
ACCOUNT_ID_KEY = "accountId"

logger = logging.getLogger(__name__)


class AwsInstance(CloudInstance):
    """
    Class which gives useful information about the current instance you're on.
    """
    def is_instance(self):
        return self.instance_id is not None

    def get_cloud_provider_name(self) -> Environment:
        return Environment.AWS

    def __init__(self):
        self.instance_id = None
        self.region = None
        self.account_id = None

        try:
            self.instance_id = urllib.request.urlopen(
                AWS_LATEST_METADATA_URI_PREFIX + 'meta-data/instance-id', timeout=2).read().decode()
            self.region = self._parse_region(
                urllib.request.urlopen(
                    AWS_LATEST_METADATA_URI_PREFIX + 'meta-data/placement/availability-zone').read().decode())
        except (urllib.error.URLError, IOError) as e:
            logger.debug("Failed init of AwsInstance while getting metadata: {}".format(e))

        try:
            self.account_id = self._extract_account_id(
                urllib.request.urlopen(
                    AWS_LATEST_METADATA_URI_PREFIX + 'dynamic/instance-identity/document', timeout=2).read().decode())
        except (urllib.error.URLError, IOError) as e:
            logger.debug("Failed init of AwsInstance while getting dynamic instance data: {}".format(e))

    @staticmethod
    def _parse_region(region_url_response):
        # For a list of regions, see:
        # https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.RegionsAndAvailabilityZones.html
        # This regex will find any AWS region format string in the response.
        re_phrase = r'((?:us|eu|ap|ca|cn|sa)-[a-z]*-[0-9])'
        finding = re.findall(re_phrase, region_url_response, re.IGNORECASE)
        if finding:
            return finding[0]
        else:
            return None

    def get_instance_id(self):
        return self.instance_id

    def get_region(self):
        return self.region

    @staticmethod
    def _extract_account_id(instance_identity_document_response):
        """
        Extracts the account id from the dynamic/instance-identity/document metadata path.
        Based on https://forums.aws.amazon.com/message.jspa?messageID=409028 which has a few more solutions,
        in case Amazon break this mechanism.
        :param instance_identity_document_response: json returned via the web page ../dynamic/instance-identity/document
        :return: The account id
        """
        return json.loads(instance_identity_document_response)[ACCOUNT_ID_KEY]

    def get_account_id(self):
        """
        :return:    the AWS account ID which "owns" this instance.
        See https://docs.aws.amazon.com/general/latest/gr/acct-identifiers.html
        """
        return self.account_id
