import argparse
import json
import logging
import logging.config
import os
import sys
import traceback
from multiprocessing import freeze_support

# dummy import for pyinstaller
# noinspection PyUnresolvedReferences
import infection_monkey.post_breach  # noqa: F401
from common.version import get_version
from infection_monkey.config import EXTERNAL_CONFIG_FILE, WormConfiguration
from infection_monkey.dropper import MonkeyDrops
from infection_monkey.model import DROPPER_ARG, MONKEY_ARG
from infection_monkey.monkey import InfectionMonkey
from infection_monkey.utils.monkey_log_path import (get_dropper_log_path,
                                                    get_monkey_log_path)

__author__ = 'itamar'

LOG = None

LOG_CONFIG = {'version': 1,
              'disable_existing_loggers': False,
              'formatters': {
                  'standard': {
                      'format':
                          '%(asctime)s [%(process)d:%(thread)d:%(levelname)s] %(module)s.%(funcName)s.%(lineno)d: %(message)s'
                  },
              },
              'handlers': {'console': {'class': 'logging.StreamHandler',
                                       'level': 'DEBUG',
                                       'formatter': 'standard'},
                           'file': {'class': 'logging.FileHandler',
                                    'level': 'DEBUG',
                                    'formatter': 'standard',
                                    'filename': None}
                           },
              'root': {'level': 'DEBUG',
                       'handlers': ['console']},
              }


def main():
    global LOG

    if 2 > len(sys.argv):
        return True
    freeze_support()  # required for multiprocessing + pyinstaller on windows
    monkey_mode = sys.argv[1]

    if not (monkey_mode in [MONKEY_ARG, DROPPER_ARG]):
        return True

    config_file = EXTERNAL_CONFIG_FILE

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-c', '--config')
    opts, monkey_args = arg_parser.parse_known_args(sys.argv[2:])
    if opts.config:
        config_file = opts.config
    if os.path.isfile(config_file):
        # using print because config can also change log locations
        print("Loading config from %s." % config_file)
        try:
            with open(config_file) as config_fo:
                json_dict = json.load(config_fo)
                WormConfiguration.from_kv(json_dict)
        except ValueError as e:
            print("Error loading config: %s, using default" % (e,))
    else:
        print("Config file wasn't supplied and default path: %s wasn't found, using internal default" % (config_file,))

    print("Loaded Configuration: %r" % WormConfiguration.hide_sensitive_info(WormConfiguration.as_dict()))

    # Make sure we're not in a machine that has the kill file
    kill_path = os.path.expandvars(
        WormConfiguration.kill_file_path_windows) if sys.platform == "win32" else WormConfiguration.kill_file_path_linux
    if os.path.exists(kill_path):
        print("Kill path found, finished run")
        return True

    try:
        if MONKEY_ARG == monkey_mode:
            log_path = get_monkey_log_path()
            monkey_cls = InfectionMonkey
        elif DROPPER_ARG == monkey_mode:
            log_path = get_dropper_log_path()
            monkey_cls = MonkeyDrops
        else:
            return True
    except ValueError:
        return True

    if WormConfiguration.use_file_logging:
        if os.path.exists(log_path):
            # If log exists but can't be removed it means other monkey is running. This usually happens on upgrade
            # from 32bit to 64bit monkey on Windows. In all cases this shouldn't be a problem.
            try:
                os.remove(log_path)
            except OSError:
                pass
        LOG_CONFIG['handlers']['file']['filename'] = log_path
        # noinspection PyUnresolvedReferences
        LOG_CONFIG['root']['handlers'].append('file')
    else:
        del LOG_CONFIG['handlers']['file']

    logging.config.dictConfig(LOG_CONFIG)
    LOG = logging.getLogger()

    def log_uncaught_exceptions(ex_cls, ex, tb):
        LOG.critical(''.join(traceback.format_tb(tb)))
        LOG.critical('{0}: {1}'.format(ex_cls, ex))

    sys.excepthook = log_uncaught_exceptions

    LOG.info(">>>>>>>>>> Initializing monkey (%s): PID %s <<<<<<<<<<",
             monkey_cls.__name__, os.getpid())

    LOG.info(f"version: {get_version()}")

    monkey = monkey_cls(monkey_args)
    monkey.initialize()

    try:
        monkey.start()

        if WormConfiguration.serialize_config:
            with open(config_file, 'w') as config_fo:
                json_dict = WormConfiguration.as_dict()
                json.dump(json_dict, config_fo, skipkeys=True, sort_keys=True, indent=4, separators=(',', ': '))

        return True
    except Exception as e:
        LOG.exception("Exception thrown from monkey's start function. More info: {}".format(e))
    finally:
        monkey.cleanup()


if "__main__" == __name__:
    if not main():
        sys.exit(1)
