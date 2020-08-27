import sys

if sys.platform.startswith("win"):
    import pythoncom

    pythoncom.CoInitialize()
    import wmi

from .mongo_utils import MongoUtils

__author__ = 'maor.rayzin'


class WMIUtils:

    def __init__(self):
        # Static class
        pass

    @staticmethod
    def get_wmi_class(class_name, moniker="//./root/cimv2", properties=None):
        _wmi = wmi.WMI(moniker=moniker)

        try:
            if not properties:
                wmi_class = getattr(_wmi, class_name)()
            else:
                wmi_class = getattr(_wmi, class_name)(properties)

        except wmi.x_wmi:
            return

        return MongoUtils.fix_obj_for_mongo(wmi_class)
