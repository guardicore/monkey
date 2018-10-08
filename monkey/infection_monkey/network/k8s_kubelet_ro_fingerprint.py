import json
import logging
from contextlib import closing
import six
import requests
from requests.exceptions import Timeout, ConnectionError

from common.str_utils import byteify
import infection_monkey.config
from infection_monkey.model.host import VictimHost
from infection_monkey.network import HostFinger
from infection_monkey.network.tools import tcp_port_to_service


K8S_KUBELET_RO_PORT = 10255
K8S_KUBELET_RO_TIMEOUT = 5

LOG = logging.getLogger(__name__)
__author__ = 'itay.mizeretz'


class K8sKubeletRoFinger(HostFinger):
    """
        Fingerprints k8s kubelet readonly server
    """

    def __init__(self):
        self._config = infection_monkey.config.WormConfiguration

    def get_host_fingerprint(self, host):
        """
        Returns k8s kubelet readonly server metadata
        :param host:
        :return: Success/failure, data is saved in the host struct
        """
        assert isinstance(host, VictimHost)
        try:
            url = 'http://%s:%s/pods' % (host.ip_addr, K8S_KUBELET_RO_PORT)
            with closing(requests.get(url, timeout=K8S_KUBELET_RO_TIMEOUT)) as req:
                data = byteify(json.loads(req.text))
                service_name = tcp_port_to_service(K8S_KUBELET_RO_PORT)
                host.services[service_name] = \
                    {
                        'name': 'k8s-kubelet-readonly',
                        'data': K8sKubeletRoFinger.parse_kubelet_response(data)
                    }
                return True
        except Timeout:
            LOG.debug("Got timeout while trying to read header information")
        except ConnectionError:  # Someone doesn't like us
            LOG.debug("Unknown connection error")
        except KeyError:
            LOG.debug("Failed parsing the k8s kubelet JSON response")
        return False

    @staticmethod
    def parse_kubelet_response(resp):
        return {'pods': [K8sKubeletRoFinger.parse_pod_item(x) for x in resp['items']]}

    @staticmethod
    def parse_pod_item(pod):
        metadata = pod['metadata']
        status = pod['status']
        spec = pod['spec']
        return \
            {
                'name': metadata['name'],
                'namespace': metadata['namespace'],
                'node_name': spec['nodeName'],
                'is_host_network': spec.get('hostNetwork', False),
                'containers': [K8sKubeletRoFinger.parse_container_item(x) for x in spec['containers']],
                'phase': status['phase'],
                'host_ip': status.get('hostIP', None),
                'pod_ip': status.get('podIP', None),
                'labels': [{'key': k, 'value': v} for (k, v) in six.iteritems(metadata['labels'])]
            }

    @staticmethod
    def parse_container_item(container):
        return \
            {
                'name': container['name'],
                'image': container['image'],
                'command': ' '.join(container.get('command', [])),
                'ports': [K8sKubeletRoFinger.parse_port_item(x) for x in container.get('ports', [])]
            }

    @staticmethod
    def parse_port_item(port):
        return port['protocol'].lower() + '-' + str(port['containerPort'])



