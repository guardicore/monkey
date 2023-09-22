import json
import logging
import re
from typing import Optional, Tuple

import requests

AWS_INSTANCE_METADATA_LOCAL_IP_ADDRESS = "169.254.169.254"
AWS_LATEST_METADATA_URI_PREFIX = f"http://{AWS_INSTANCE_METADATA_LOCAL_IP_ADDRESS}/latest/"
ACCOUNT_ID_KEY = "accountId"

logger = logging.getLogger(__name__)

AWS_TIMEOUT = 2


def fetch_aws_instance_metadata() -> Tuple[Optional[str], Optional[str], Optional[str]]:
    instance_id = None
    region = None
    account_id = None

    try:
        instance_id = _fetch_aws_instance_id()
        region = _fetch_aws_region()
        account_id = _fetch_account_id()
    except (
        requests.RequestException,
        IOError,
        json.decoder.JSONDecodeError,
    ) as err:
        logger.debug(f"Failed init of AWSInstance while getting metadata: {err}")
        return (None, None, None)

    return (instance_id, region, account_id)


def _fetch_aws_instance_id() -> Optional[str]:
    url = AWS_LATEST_METADATA_URI_PREFIX + "meta-data/instance-id"
    response = requests.get(
        url,
        timeout=AWS_TIMEOUT,
    )
    response.raise_for_status()

    return response.text


def _fetch_aws_region() -> Optional[str]:
    response = requests.get(
        AWS_LATEST_METADATA_URI_PREFIX + "meta-data/placement/availability-zone",
        timeout=AWS_TIMEOUT,
    )
    response.raise_for_status()

    return _parse_region(response.text)


def _parse_region(region_url_response: str) -> Optional[str]:
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


def _fetch_account_id() -> str:
    """
    Fetches and extracts the account id from the dynamic/instance-identity/document metadata path.
    Based on https://forums.aws.amazon.com/message.jspa?messageID=409028 which has a few more
    solutions, in case Amazon break this mechanism.
    :param instance_identity_document_response: json returned via the web page
    ../dynamic/instance-identity/document
    :return: The account id
    """
    response = requests.get(
        AWS_LATEST_METADATA_URI_PREFIX + "dynamic/instance-identity/document",
        timeout=AWS_TIMEOUT,
    )
    response.raise_for_status()

    return json.loads(response.text)[ACCOUNT_ID_KEY]
