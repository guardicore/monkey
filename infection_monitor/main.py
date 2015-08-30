
import time
import logging
from config import MonitorConfiguration

__author__ = 'itamar'

logging.basicConfig(format='%(asctime)s [%(process)d:%(levelname)s] %(module)s.%(funcName)s.%(lineno)d: %(message)s',
                    level=logging.DEBUG)
LOG = logging.getLogger()

def do_infected():
    LOG.info("Changed state to infected")

    [action.do_action()
    for action in MonitorConfiguration.actions]

def do_not_infected():
    LOG.info("Changed state to not infected")
    [action.undo_action()
    for action in MonitorConfiguration.actions]

def main():
    infected = False

    LOG.info("Monitor going up...")

    do_not_infected()

    try:
        while True:
            if any([condition.check_condition()
                   for condition in MonitorConfiguration.conditions]):
                if not infected:
                    do_infected()

                infected = True
            else:
                if infected:
                    do_not_infected()

                infected = False

            for _ in range(MonitorConfiguration.monitor_interval / 1000):
                time.sleep(1.0)
    finally:
        if infected:
            do_not_infected()

        LOG.info("Monitor going down...")


if "__main__" == __name__:
    main()
