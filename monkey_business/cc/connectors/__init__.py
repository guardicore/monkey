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

    def log(self, text):
        pass

    def set_logger(self, logger):
        self.log = logger

class NetControllerJob(object):
    connector_type = NetControllerConnector
    _connector = None
    _logger = None

    _properties = {
        # property: value
    }

    _enumerations = {

    }

    def __init__(self, existing_connector=None, logger=None):
        self._connector = existing_connector
        self._logger = logger
        if logger:
            self._connector.set_logger(self.log)

    def log(self, text):
        if self._logger:
            self._logger.log(text)

    # external API

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

    def get_state(self):
        return None

    def stop(self):
        raise NotImplementedError()