import pkgutil
import sys
from pathlib import PurePath

_scoutsuite_api_package = pkgutil.get_loader('infection_monkey.system_info.collectors.'
                                             'scoutsuite_collector.scoutsuite.ScoutSuite.__main__')


def _add_scoutsuite_to_python_path():
    scoutsuite_path = PurePath(_scoutsuite_api_package.path).parent.parent.__str__()
    sys.path.append(scoutsuite_path)


_add_scoutsuite_to_python_path()

import infection_monkey.system_info.collectors.scoutsuite_collector.scoutsuite.ScoutSuite.api_run as scoutsuite_api


def run(*args, **kwargs):
    return scoutsuite_api.run(*args, **kwargs)
