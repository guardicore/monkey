import os
import sys
import logging
import traceback
import logging.config
from config import WormConfiguration, EXTERNAL_CONFIG_FILE
from model import MONKEY_ARG, DROPPER_ARG
from dropper import MonkeyDrops
from monkey import ChaosMonkey
import argparse
import json

if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

__author__ = 'itamar'

LOG = None

LOG_CONFIG = {'version': 1,
              'disable_existing_loggers': False,
              'formatters': {'standard': {'format': '%(asctime)s [%(process)d:%(levelname)s] %(module)s.%(funcName)s.%(lineno)d: %(message)s'},
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

    monkey_mode = sys.argv[1]

    if not monkey_mode in [MONKEY_ARG, DROPPER_ARG]:
        return True

    config_file = EXTERNAL_CONFIG_FILE

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-c', '--config')
    opts, monkey_args = arg_parser.parse_known_args(sys.argv[2:])
    if opts.config:
        config_file = opts.config
    if os.path.isfile(config_file):
        # using print because config can also change log locations
        print "Loading config from %s." % config_file
        try:
            with open(config_file) as config_fo:
                json_dict = json.load(config_fo)
                WormConfiguration.from_dict(json_dict)
                print "Configuration loaded: %r" % WormConfiguration.as_dict()
        except ValueError as e:
            print "Error loading config, using default: %s" % e
    else:
        LOG.warning("Config file: %s wasn't found, using default" % config_file)

    try:
        if MONKEY_ARG == monkey_mode:
            log_path = WormConfiguration.monkey_log_path
            monkey_cls = ChaosMonkey
        elif DROPPER_ARG == monkey_mode:
            log_path = WormConfiguration.dropper_log_path
            monkey_cls = MonkeyDrops
        else:
            return True
    except ValueError:
        return True

    if WormConfiguration.use_file_logging:
        LOG_CONFIG['handlers']['file']['filename'] = log_path
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

    monkey = monkey_cls(monkey_args)
    monkey.initialize()

    try:
        monkey.start()

        if WormConfiguration.serialize_config:
          with open(config_file, 'w') as config_fo:
            json_dict = WormConfiguration.as_dict()
            json.dump(json_dict, config_fo, skipkeys=True, sort_keys=True, indent=4, separators=(',', ': '))
          
        return True
    finally:
        monkey.cleanup()

if "__main__" == __name__:
    if not main():
        sys.exit(1)
