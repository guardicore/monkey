import json
import logging
import re

import requests

AWS_INSTANCE_METADATA_LOCAL_IP_ADDRESS = "169.254.169.254"
AWS_LATEST_METADATA_URI_PREFIX = f"http://{AWS_INSTANCE_METADATA_LOCAL_IP_ADDRESS}/latest/"
ACCOUNT_ID_KEY = "accountId"

logger = logging.getLogger(__name__)

AWS_TIMEOUT = 2


def fetch_aws_instance_metadata():
    instance_id = None
    region = None
    account_id = None

    try:
        response = requests.get(
            AWS_LATEST_METADATA_URI_PREFIX + "meta-data/instance-id",
            timeout=AWS_TIMEOUT,
        )
        if not response:
            return (None, None, None)

        instance_id = response.text

        region = _parse_region(
            requests.get(
                AWS_LATEST_METADATA_URI_PREFIX + "meta-data/placement/availability-zone",
                timeout=AWS_TIMEOUT,
            ).text
        )

        account_id = _extract_account_id(
            requests.get(
                AWS_LATEST_METADATA_URI_PREFIX + "dynamic/instance-identity/document",
                timeout=AWS_TIMEOUT,
            ).text
        )
    except (requests.RequestException, IOError, json.decoder.JSONDecodeError) as err:
        logger.debug(f"Failed init of AWSInstance while getting metadata: {err}")
        return (None, None, None)

    return (instance_id, region, account_id)


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
