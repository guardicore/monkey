import winreg

from common.utils.mongo_utils import MongoUtils

__author__ = 'maor.rayzin'


class RegUtils:

    def __init__(self):
        # Static class
        pass

    @staticmethod
    def get_reg_key(subkey_path, store=winreg.HKEY_LOCAL_MACHINE):
        key = winreg.ConnectRegistry(None, store)
        subkey = winreg.OpenKey(key, subkey_path)

        d = dict([winreg.EnumValue(subkey, i)[:2] for i in range(winreg.QueryInfoKey(subkey)[0])])
        d = MongoUtils.fix_obj_for_mongo(d)

        subkey.Close()
        key.Close()

        return d
