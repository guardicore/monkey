import pkgutil
import sys
from pathlib import PurePath

_scoutsuite_api_package = pkgutil.get_loader('common.cloud.scoutsuite.ScoutSuite.__main__')


def _add_scoutsuite_to_python_path():
    scoutsuite_path = PurePath(_scoutsuite_api_package.path).parent.parent.__str__()
    sys.path.append(scoutsuite_path)


# Add ScoutSuite to python path because this way
# we don't need to change any imports in ScoutSuite code
_add_scoutsuite_to_python_path()

import common.cloud.scoutsuite.ScoutSuite.api_run as scoutsuite_api


def run(*args, **kwargs):
    return scoutsuite_api.run(*args, **kwargs)
