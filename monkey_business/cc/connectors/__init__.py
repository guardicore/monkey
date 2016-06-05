def _load_prop_dict(self, target, prop):
    for property in prop:
        if not target.has_key(property):
            continue
        if type(prop[property]) is dict:
            _load_prop_dict(self, target[property], prop[property])
        else:
            target[property] = prop[property]


class NetControllerConnector(object):
    def __init__(self):
        self._properties = {}

    def is_connected(self):
        return False

    def connect(self):
        return

    def get_properties(self):
        return self._properties

    def load_properties(self, properties):
        _load_prop_dict(self, self._properties, properties)

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
    _properties = {
        # property: value
    }

    _enumerations = {

    }

    def __init__(self, existing_connector = None):
        if existing_connector:
            self.connector = existing_connector

    def get_job_properties(self):
        return self._properties

    def load_job_properties(self, properties):
        _load_prop_dict(self, self._properties, properties)

    def get_property_function(self, property):
        if property in self._enumerations.keys():
            return self._enumerations[property]
        return None

    def run(self):
        raise NotImplementedError()

    def get_results(self):
        return []