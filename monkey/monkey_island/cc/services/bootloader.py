from typing import Dict, List

from monkey_island.cc.database import mongo
from monkey_island.cc.services.node import NodeService
from monkey_island.cc.services.utils.node_groups import NodeGroups
from monkey_island.cc.services.utils.bootloader_config import SUPPORTED_WINDOWS_VERSIONS, MIN_GLIBC_VERSION


class BootloaderService:

    @staticmethod
    def parse_bootloader_data(data: Dict) -> bool:
        data['ips'] = BootloaderService.remove_local_ips(data['ips'])
        if data['os_version'] == "":
            data['os_version'] = "Unknown OS"
        mongo.db.bootloader_telems.insert(data)
        will_monkey_run = BootloaderService.is_os_compatible(data)
        node = NodeService.get_or_create_node_from_bootloader_data(data, will_monkey_run)
        group_keywords = [data['system'], 'monkey']
        group_keywords.append('starting') if will_monkey_run else group_keywords.append('old')
        NodeService.set_node_group(node['_id'], NodeGroups.get_group_by_keywords(group_keywords))
        return will_monkey_run

    @staticmethod
    def is_os_compatible(bootloader_data) -> bool:
        if bootloader_data['system'] == 'windows':
            return BootloaderService.is_windows_version_supported(bootloader_data['os_version'])
        elif bootloader_data['system'] == 'linux':
            return BootloaderService.is_glibc_supported(bootloader_data['glibc_version'])

    @staticmethod
    def is_windows_version_supported(windows_version) -> bool:
        return SUPPORTED_WINDOWS_VERSIONS.get(windows_version)


    @staticmethod
    def is_glibc_supported(glibc_version_string) -> bool:
        glibc_version_string = glibc_version_string.lower()
        glibc_version = glibc_version_string.split(' ')[-1]
        return glibc_version >= str(MIN_GLIBC_VERSION) and 'eglibc' not in glibc_version_string

    @staticmethod
    def remove_local_ips(ip_list) -> List[str]:
        return [i for i in ip_list if not i.startswith("127")]
