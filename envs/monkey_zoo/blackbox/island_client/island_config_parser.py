import json
import os


class IslandConfigParser(object):

    def __init__(self, config_filename):
        self.config_raw = open(IslandConfigParser.get_conf_file_path(config_filename), 'r').read()
        self.config_json = json.loads(self.config_raw)

    def get_ips_of_targets(self):
        return self.config_json['basic_network']['scope']['subnet_scan_list']

    @staticmethod
    def get_conf_file_path(conf_file_name):
        return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "island_configs",
                            conf_file_name)
