import base64
import json
import logging
from dataclasses import dataclass, field
from pathlib import PurePath
from typing import Optional, Set

logger = logging.getLogger(__name__)


@dataclass
class ChromeBrowserLocalState:
    """
    The local state for a Chrome-based browser

    This is stored in a file named "Local State" in the browser's local data directory
    """

    profile_names: Set[str] = field(default_factory=set)
    master_key: Optional[bytes] = None


def parse_local_state_file(local_state_file_path: PurePath) -> ChromeBrowserLocalState:
    """
    Parse the local state file for a Chrome-based browser
    """

    local_state = ChromeBrowserLocalState()
    try:
        with open(local_state_file_path) as f:
            local_state_object = json.load(f)
            local_state.profile_names = set(local_state_object["profile"]["info_cache"].keys())
            local_state.master_key = base64.b64decode(
                local_state_object["os_crypt"]["encrypted_key"]
            )
    except FileNotFoundError:
        logger.error(f'Couldn\'t find local state file at "{local_state_file_path}"')
    except json.decoder.JSONDecodeError as err:
        logger.error(f'Couldn\'t deserialize JSON file at "{local_state_file_path}": {err}')
    except KeyError as err:
        logger.error(
            f"Exception encountered while trying to parse the browser's local state state: {err}"
        )
    finally:
        return local_state
