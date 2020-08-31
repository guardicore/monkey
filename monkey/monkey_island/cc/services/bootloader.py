from typing import Dict, List

from bson import ObjectId

from monkey_island.cc.database import mongo
from monkey_island.cc.services.node import NodeCreationException, NodeService
from monkey_island.cc.services.utils.bootloader_config import (
    MIN_GLIBC_VERSION, SUPPORTED_WINDOWS_VERSIONS)
from monkey_island.cc.services.utils.node_states import NodeStates


class BootloaderService:

    @staticmethod
    def parse_bootloader_telem(telem: Dict) -> bool:
        telem['ips'] = BootloaderService.remove_local_ips(telem['ips'])
        if telem['os_version'] == "":
            telem['os_version'] = "Unknown OS"

        telem_id = BootloaderService.get_mongo_id_for_bootloader_telem(telem)
        mongo.db.bootloader_telems.update({'_id': telem_id}, {'$setOnInsert': telem}, upsert=True)

        will_monkey_run = BootloaderService.is_os_compatible(telem)
        try:
            node = NodeService.get_or_create_node_from_bootloader_telem(telem, will_monkey_run)
        except NodeCreationException:
            # Didn't find the node, but allow monkey to run anyways
            return True

        node_group = BootloaderService.get_next_node_state(node, telem['system'], will_monkey_run)
        if 'group' not in node or node['group'] != node_group.value:
            NodeService.set_node_group(node['_id'], node_group)
        return will_monkey_run

    @staticmethod
    def get_next_node_state(node: Dict, system: str, will_monkey_run: bool) -> NodeStates:
        group_keywords = [system, 'monkey']
        if 'group' in node and node['group'] == 'island':
            group_keywords.extend(['island', 'starting'])
        else:
            group_keywords.append('starting') if will_monkey_run else group_keywords.append('old')
        node_group = NodeStates.get_by_keywords(group_keywords)
        return node_group

    @staticmethod
    def get_mongo_id_for_bootloader_telem(bootloader_telem) -> ObjectId:
        ip_hash = hex(hash(str(bootloader_telem['ips'])))[3:15]
        hostname_hash = hex(hash(bootloader_telem['hostname']))[3:15]
        return ObjectId(ip_hash + hostname_hash)

    @staticmethod
    def is_os_compatible(bootloader_data) -> bool:
        if bootloader_data['system'] == 'windows':
            return BootloaderService.is_windows_version_supported(bootloader_data['os_version'])
        elif bootloader_data['system'] == 'linux':
            return BootloaderService.is_glibc_supported(bootloader_data['glibc_version'])

    @staticmethod
    def is_windows_version_supported(windows_version) -> bool:
        return SUPPORTED_WINDOWS_VERSIONS.get(windows_version, True)

    @staticmethod
    def is_glibc_supported(glibc_version_string) -> bool:
        glibc_version_string = glibc_version_string.lower()
        glibc_version = glibc_version_string.split(' ')[-1]
        return glibc_version >= str(MIN_GLIBC_VERSION) and 'eglibc' not in glibc_version_string

    @staticmethod
    def remove_local_ips(ip_list) -> List[str]:
        return [i for i in ip_list if not i.startswith("127")]
