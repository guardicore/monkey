
class NetControllerConnector(object):
    def __init__(self):
        self._properties = {}

    def _load_prop_dict(self, target, prop):
        for property in prop:
            if not target.has_key(property):
                continue
            if type(prop[property]) is dict:
                self._load_prop_dict(target[property], prop[property])
            else:
                target[property] = prop[property]

    def is_connected(self):
        return False

    def connect(self):
        return

    def get_properties(self):
        return self._properties

    def load_properties(self, properties):
        self._load_prop_dict(self._properties, properties)

    def get_vlans_list(self):
        raise NotImplementedError()

    def get_entities_on_vlan(self, vlanid):
        raise NotImplementedError()

    def deploy_monkey(self, vlanid):
        raise NotImplementedError()

    def disconnect(self):
        return

class NetControllerJob(object):
    connector = NetControllerConnector

    def __init__(self):
        self._properties = {
            # property: [value, enumerating_function]
        }

    def get_job_properties(self):
        return self._properties

    def set_job_properties(self, properties):
        return {}

    def run(self):
        raise NotImplementedError()