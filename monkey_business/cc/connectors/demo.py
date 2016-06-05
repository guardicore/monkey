from connectors import NetControllerJob, NetControllerConnector

demo_state = {
    501: ["Machine A", "Machine B"],
    502: ["Machine C",],
    503: ["Machine D",],
    514: ["Machine E", "Machine F"],
}

class DemoConnector(NetControllerConnector):
    def __init__(self):
        self._conn = None
        self._properties = {
            "address": "127.0.0.1",
            "port": 0,
            "username": "",
            "password": "",
        }

    def connect(self):
        self._conn = object()

    def is_connected(self):
        return not self._conn == None

    def disconnect(self):
        self._conn = None

    def get_vlans_list(self):
        return demo_state.keys()

    def get_entities_on_vlan(self, vlanid):
        if (demo_state.has_key(vlanid)):
            return demo_state[vlanid]
        return []

class DemoJob(NetControllerJob):
    connector_type = DemoConnector
    _properties = {
        "vlan": 0,
    }
    _enumerations = {
        "vlan": "get_vlans_list",
    }

    def run(self):
        import time
        self.log("Running demo job...")
        time.sleep(30)