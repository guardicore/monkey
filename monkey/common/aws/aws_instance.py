import json
import logging
import re
from dataclasses import dataclass
from typing import Optional, Tuple

import requests

AWS_INSTANCE_METADATA_LOCAL_IP_ADDRESS = "169.254.169.254"
AWS_LATEST_METADATA_URI_PREFIX = "http://{0}/latest/".format(AWS_INSTANCE_METADATA_LOCAL_IP_ADDRESS)
ACCOUNT_ID_KEY = "accountId"

logger = logging.getLogger(__name__)

AWS_TIMEOUT = 2


@dataclass
class AwsInstanceInfo:
    instance_id: Optional[str] = None
    region: Optional[str] = None
    account_id: Optional[str] = None


class AwsInstance:
    """
    Class which gives useful information about the current instance you're on.
    """

    def __init__(self):
        self._is_instance, self._instance_info = AwsInstance._fetch_instance_info()

    @property
    def is_instance(self) -> bool:
        return self._is_instance

    @property
    def instance_id(self) -> str:
        return self._instance_info.instance_id

    @property
    def region(self) -> str:
        return self._instance_info.region

    @property
    def account_id(self) -> str:
        return self._instance_info.account_id

    @staticmethod
    def _fetch_instance_info() -> Tuple[bool, AwsInstanceInfo]:
        try:
            response = requests.get(
                AWS_LATEST_METADATA_URI_PREFIX + "meta-data/instance-id",
                timeout=AWS_TIMEOUT,
            )
            if not response:
                return False, AwsInstanceInfo()

            info = AwsInstanceInfo()
            info.instance_id = response.text if response else False
            info.region = AwsInstance._parse_region(
                requests.get(
                    AWS_LATEST_METADATA_URI_PREFIX + "meta-data/placement/availability-zone",
                    timeout=AWS_TIMEOUT,
                ).text
            )
        except (requests.RequestException, IOError) as e:
            logger.debug("Failed init of AwsInstance while getting metadata: {}".format(e))
            return False, AwsInstanceInfo()

        try:
            info.account_id = AwsInstance._extract_account_id(
                requests.get(
                    AWS_LATEST_METADATA_URI_PREFIX + "dynamic/instance-identity/document",
                    timeout=AWS_TIMEOUT,
                ).text
            )
        except (requests.RequestException, json.decoder.JSONDecodeError, IOError) as e:
            logger.debug(
                "Failed init of AwsInstance while getting dynamic instance data: {}".format(e)
            )
            return False, AwsInstanceInfo()

        return True, info

    @staticmethod
    def _parse_region(region_url_response):
        # For a list of regions, see:
        # https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts
        # .RegionsAndAvailabilityZones.html
        # This regex will find any AWS region format string in the response.
        re_phrase = r"((?:us|eu|ap|ca|cn|sa)-[a-z]*-[0-9])"
        finding = re.findall(re_phrase, region_url_response, re.IGNORECASE)
        if finding:
            return finding[0]
        else:
            return None

    @staticmethod
    def _extract_account_id(instance_identity_document_response):
        """
        Extracts the account id from the dynamic/instance-identity/document metadata path.
        Based on https://forums.aws.amazon.com/message.jspa?messageID=409028 which has a few more
        solutions,
        in case Amazon break this mechanism.
        :param instance_identity_document_response: json returned via the web page
        ../dynamic/instance-identity/document
        :return: The account id
        """
        return json.loads(instance_identity_document_response)[ACCOUNT_ID_KEY]

    def get_account_id(self):
        """
        :return:    the AWS account ID which "owns" this instance.
        See https://docs.aws.amazon.com/general/latest/gr/acct-identifiers.html
        """
        return self.account_id
