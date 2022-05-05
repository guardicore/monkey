import threading

from common.aws.aws_metadata import fetch_aws_instance_metadata

AWS_FETCH_METADATA_TIMEOUT = 10.0  # Seconds


class AWSTimeoutError(Exception):
    """Raised when communications with AWS timeout"""


class AWSInstance:
    """
    Class which gives useful information about the current instance you're on.
    """

    def __init__(self):
        self._instance_id = None
        self._region = None
        self._account_id = None
        self._initialization_complete = threading.Event()

        fetch_thread = threading.Thread(target=self._fetch_aws_instance_metadata, daemon=True)
        fetch_thread.start()

    def _fetch_aws_instance_metadata(self):
        metadata = fetch_aws_instance_metadata()
        self._instance_id = metadata[0]
        self._region = metadata[1]
        self._account_id = metadata[2]

        self._initialization_complete.set()

    @property
    def is_instance(self) -> bool:
        self._wait_for_initialization_to_complete()
        return self._instance_id is not None

    @property
    def instance_id(self) -> str:
        self._wait_for_initialization_to_complete()
        return self._instance_id

    @property
    def region(self) -> str:
        self._wait_for_initialization_to_complete()
        return self._region

    @property
    def account_id(self) -> str:
        self._wait_for_initialization_to_complete()
        return self._account_id

    def _wait_for_initialization_to_complete(self):
        if not self._initialization_complete.wait(AWS_FETCH_METADATA_TIMEOUT):
            raise AWSTimeoutError("Timed out while attempting to retrieve metadata from AWS")
