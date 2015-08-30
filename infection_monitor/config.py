
import sys
from condition import FilesExistCondition
from action import ChangeDesktopAction

__author__ = 'itamar'


class MonitorConfiguration(object):
    conditions = [FilesExistCondition(r"C:\windows\monkey.exe"),
                  ]

    actions = [ChangeDesktopAction(r"infected.bmp")
               ]

    monitor_interval = 5000 # 5 seconds
