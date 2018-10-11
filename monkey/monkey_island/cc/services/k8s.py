from cc.database import mongo
from cc.services.config import ConfigService
from cc.services.edge import EdgeService
from cc.services.node import NodeService

__author__ = "itay.mizeretz"


class K8sService:
    def __init__(self):
        pass

    @staticmethod
    def handle_new_pod(pod):
        """
        Adds info to new/existing nodes and adds new scanning targets.
        :param pod: Newly discovered pod
        :return: None
        """
        pod_ip = pod.pop('pod_ip')  # We don't want to add the pod_ip to db because it's useless at this point.
        host_ip = pod['host_ip']
        pod_node = None
        host_node = None
        if pod_ip:
            pod_node = NodeService.get_or_create_node(pod_ip)
            if pod['is_host_network']:
                K8sService._add_host_pod_info(pod_node['_id'], pod)
            else:
                K8sService._set_pod_info(pod_node['_id'], pod)
                K8sService.add_k8s_machine_to_scan_list(pod_ip)

        if host_ip:
            host_node = NodeService.get_or_create_node(host_ip)
            K8sService._set_node_name(host_node['_id'], pod['node_name'])
            if not pod['is_host_network']:
                K8sService._add_pod_ip_to_host(host_node['_id'], pod_ip)
                K8sService.add_k8s_machine_to_scan_list(host_ip)

        if pod_node and host_node and not pod['is_host_network']:
            EdgeService.insert_host_edge(host_node['_id'], pod_node['_id'], pod_ip)

    @staticmethod
    def add_k8s_machine_to_scan_list(machine_ip):
        """
        Adds a k8s pod/node to scan list (if allowed by config).
        :param machine_ip: IP of pod/node to add
        :return: None
        """
        if ConfigService.get_config_value(['basic_network', 'general', 'k8s_pod_scan']):
            ConfigService.add_item_to_config_set('internal.general.dynamic_subnet_scan_list', machine_ip)

    @staticmethod
    def _add_pod_ip_to_host(host_id, pod_ip):
        mongo.db.node.update({'_id': host_id}, {'$addToSet': {'k8s_node.pod_ips': pod_ip}})

    @staticmethod
    def _set_node_name(host_id, node_name):
        mongo.db.node.update({'_id': host_id}, {'$set': {'k8s_node.name': node_name}})

    @staticmethod
    def _set_pod_info(pod_id, pod):
        mongo.db.node.update({'_id': pod_id}, {'$set': {'k8s_pod': pod}})

    @staticmethod
    def _add_host_pod_info(host_id, pod):
        mongo.db.node.update({'_id': host_id}, {'$addToSet': {'k8s_host_pods': pod}})
