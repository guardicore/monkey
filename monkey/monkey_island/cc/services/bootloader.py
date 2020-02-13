from typing import Dict, List

from monkey_island.cc.database import mongo
from monkey_island.cc.services.node import NodeService
from monkey_island.cc.services.utils.node_groups import NodeGroups

WINDOWS_VERSIONS = {
    "5.0": "Windows 2000",
    "5.1": "Windows XP",
    "5.2": "Windows XP/server 2003",
    "6.0": "Windows Vista/server 2008",
    "6.1": "Windows 7/server 2008R2",
    "6.2": "Windows 8/server 2012",
    "6.3": "Windows 8.1/server 2012R2",
    "10.0": "Windows 10/server 2016-2019"
}

MIN_GLIBC_VERSION = 2.14


class BootloaderService:

    @staticmethod
    def parse_bootloader_data(data: Dict) -> str:
        data['ips'] = BootloaderService.remove_local_ips(data['ips'])
        mongo.db.bootloader_telems.insert(data)
        will_monkey_run = BootloaderService.is_glibc_supported(data['glibc_version'])
        node = NodeService.get_or_create_node_from_bootloader_data(data, will_monkey_run)
        group_keywords = [data['system'], 'monkey']
        group_keywords.append('starting') if will_monkey_run else group_keywords.append('old')
        NodeService.set_node_group(node['_id'], NodeGroups.get_group_by_keywords(group_keywords))
        return "abc"

    @staticmethod
    def is_glibc_supported(glibc_version_string) -> bool:
        glibc_version_string = glibc_version_string.lower()
        glibc_version = glibc_version_string.split(' ')[-1]
        return glibc_version >= str(MIN_GLIBC_VERSION) and 'eglibc' not in glibc_version_string

    @staticmethod
    def remove_local_ips(ip_list) -> List[str]:
        return [i for i in ip_list if not i.startswith("127")]
