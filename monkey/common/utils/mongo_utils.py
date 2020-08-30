import sys

if sys.platform == 'win32':
    import win32com
    import wmi

__author__ = 'maor.rayzin'


class MongoUtils:

    def __init__(self):
        # Static class
        pass

    @staticmethod
    def fix_obj_for_mongo(o):
        if isinstance(o, dict):
            return dict([(k, MongoUtils.fix_obj_for_mongo(v)) for k, v in list(o.items())])

        elif type(o) in (list, tuple):
            return [MongoUtils.fix_obj_for_mongo(i) for i in o]

        elif type(o) in (int, float, bool):
            return o

        elif isinstance(o, str):
            # mongo doesn't like unprintable chars, so we use repr :/
            return repr(o)

        elif hasattr(o, "__class__") and o.__class__ == wmi._wmi_object:
            return MongoUtils.fix_wmi_obj_for_mongo(o)

        elif hasattr(o, "__class__") and o.__class__ == win32com.client.CDispatch:
            try:
                # objectSid property of ds_user is problematic and need this special treatment.
                # ISWbemObjectEx interface. Class Uint8Array ?
                if str(o._oleobj_.GetTypeInfo().GetTypeAttr().iid) == "{269AD56A-8A67-4129-BC8C-0506DCFE9880}":
                    return o.Value
            except:
                pass

            try:
                return o.GetObjectText_()
            except:
                pass

            return repr(o)

        else:
            return repr(o)

    @staticmethod
    def fix_wmi_obj_for_mongo(o):
        row = {}

        for prop in o.properties:
            try:
                value = getattr(o, prop)
            except wmi.x_wmi:
                # This happens in Win32_GroupUser when the user is a domain user.
                # For some reason, the wmi query for PartComponent fails. This table
                # is actually contains references to Win32_UserAccount and Win32_Group.
                # so instead of reading the content to the Win32_UserAccount, we store
                # only the id of the row in that table, and get all the other information
                # from that table while analyzing the data.
                value = o.properties[prop].value

            row[prop] = MongoUtils.fix_obj_for_mongo(value)

        for method_name in o.methods:
            if not method_name.startswith("GetOwner"):
                continue

            method = getattr(o, method_name)

            try:
                value = method()
                value = MongoUtils.fix_obj_for_mongo(value)
                row[method_name[3:]] = value

            except wmi.x_wmi:
                continue

        return row
