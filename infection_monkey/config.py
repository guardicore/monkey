import os
import struct
import sys
import types
import uuid
from abc import ABCMeta
from itertools import product

from exploit import WmiExploiter, Ms08_067_Exploiter, SmbExploiter, RdpExploiter, SSHExploiter, ShellShockExploiter, \
    SambaCryExploiter, ElasticGroovyExploiter
from network import TcpScanner, PingScanner, SMBFinger, SSHFinger, HTTPFinger, MySQLFinger, ElasticFinger

__author__ = 'itamar'

GUID = str(uuid.getnode())

EXTERNAL_CONFIG_FILE = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'monkey.bin')


def _cast_by_example(value, example):
    """
    a method that casts a value to the type of the parameter given as example
    """
    example_type = type(example)
    if example_type is str:
        return os.path.expandvars(value).encode("utf8")
    elif example_type is tuple and len(example) != 0:
        if value is None or value == tuple([None]):
            return tuple()
        return tuple([_cast_by_example(x, example[0]) for x in value])
    elif example_type is list and len(example) != 0:
        if value is None or value == [None]:
            return []
        return [_cast_by_example(x, example[0]) for x in value]
    elif example_type is type(value):
        return value
    elif example_type is bool:
        return value.lower() == 'true'
    elif example_type is int:
        return int(value)
    elif example_type is float:
        return float(value)
    elif example_type in (type, ABCMeta):
        return globals()[value]
    else:
        return None


class Configuration(object):
    def from_dict(self, data):
        """
        Get a dict of config variables, set known variables as attributes on self.
        Return dict of unknown variables encountered.
        """
        unknown_variables = {}
        for key, value in data.items():
            if key.startswith('_'):
                continue
            if key in ["name", "id", "current_server"]:
                continue
            if self._depth_from_commandline and key == "depth":
                continue
            try:
                default_value = getattr(Configuration, key)
            except AttributeError:
                unknown_variables[key] = value
                continue

            setattr(self, key, _cast_by_example(value, default_value))
        return unknown_variables

    def as_dict(self):
        result = {}
        for key in dir(Configuration):
            if key.startswith('_'):
                continue
            try:
                value = getattr(self, key)
            except AttributeError:
                continue

            val_type = type(value)

            if val_type is types.FunctionType or val_type is types.MethodType:
                continue

            if val_type in (type, ABCMeta):
                value = value.__name__
            elif val_type is tuple or val_type is list:
                if len(value) != 0 and type(value[0]) in (type, ABCMeta):
                    value = val_type([x.__name__ for x in value])

            result[key] = value

        return result

    # Used to keep track of our depth if manually specified
    _depth_from_commandline = False

    ###########################
    # logging config
    ###########################

    use_file_logging = True
    dropper_log_path_windows = '%temp%\\~df1562.tmp'
    dropper_log_path_linux = '/tmp/user-1562'
    monkey_log_path_windows = '%temp%\\~df1563.tmp'
    monkey_log_path_linux = '/tmp/user-1563'
    send_log_to_server = True

    ###########################
    # dropper config
    ###########################

    dropper_try_move_first = True
    dropper_set_date = True
    dropper_date_reference_path_windows = r"%windir%\system32\kernel32.dll"
    dropper_date_reference_path_linux = '/bin/sh'
    dropper_target_path_win_32 = r"C:\Windows\monkey32.exe"
    dropper_target_path_win_64 = r"C:\Windows\monkey64.exe"
    dropper_target_path_linux = '/tmp/monkey'

    ###########################
    # Kill file
    ###########################
    kill_file_path_windows = '%windir%\\monkey.not'
    kill_file_path_linux = '/var/run/monkey.not'

    ###########################
    # monkey config
    ###########################
    # sets whether or not the monkey is alive. if false will stop scanning and exploiting
    alive = True

    # sets whether or not to self delete the monkey executable when stopped
    self_delete_in_cleanup = False

    # string of the mutex name for single instance
    singleton_mutex_name = "{2384ec59-0df8-4ab9-918c-843740924a28}"

    # how long to wait between scan iterations
    timeout_between_iterations = 100

    # how many scan iterations to perform on each run
    max_iterations = 1

    scanner_class = TcpScanner
    finger_classes = [SMBFinger, SSHFinger, PingScanner, HTTPFinger, MySQLFinger, ElasticFinger]
    exploiter_classes = [SmbExploiter, WmiExploiter,  # Windows exploits
                         SSHExploiter, ShellShockExploiter, SambaCryExploiter,  # Linux
                         ElasticGroovyExploiter,  # multi
                         ]

    # how many victims to look for in a single scan iteration
    victims_max_find = 30

    # how many victims to exploit before stopping
    victims_max_exploit = 7

    # depth of propagation
    depth = 2
    current_server = ""

    # Configuration servers to try to connect to, in this order.
    command_servers = [
        "41.50.73.31:5000"
    ]

    # sets whether or not to locally save the running configuration after finishing
    serialize_config = False

    # sets whether or not to retry failed hosts on next scan
    retry_failed_explotation = True

    # addresses of internet servers to ping and check if the monkey has internet acccess.
    internet_services = ["monkey.guardicore.com", "www.google.com"]

    keep_tunnel_open_time = 60

    ###########################
    # scanners config
    ###########################

    # Auto detect and scan local subnets
    local_network_scan = True

    subnet_scan_list = ['', ]

    blocked_ips = ['', ]

    # TCP Scanner
    HTTP_PORTS = [80, 8080, 443,
                  8008,  # HTTP alternate
                  ]
    tcp_target_ports = [22,
                        2222,
                        445,
                        135,
                        3389,
                        80,
                        8080,
                        443,
                        8008,
                        3306,
                        9200]
    tcp_target_ports.extend(HTTP_PORTS)
    tcp_scan_timeout = 3000  # 3000 Milliseconds
    tcp_scan_interval = 200
    tcp_scan_get_banner = True

    # Ping Scanner
    ping_scan_timeout = 1000

    ###########################
    # exploiters config
    ###########################

    skip_exploit_if_file_exist = False

    ms08_067_exploit_attempts = 5
    ms08_067_remote_user_add = "Monkey_IUSER_SUPPORT"
    ms08_067_remote_user_pass = "Password1!"

    # rdp exploiter
    rdp_use_vbs_download = True

    # User and password dictionaries for exploits.

    def get_exploit_user_password_pairs(self):
        """
        Returns all combinations of the configurations users and passwords
        :return:
        """
        return product(self.exploit_user_list, self.exploit_password_list)

    def get_exploit_user_password_or_hash_product(self):
        """
        Returns all combinations of the configurations users and passwords or lm/ntlm hashes
        :return:
        """
        cred_list = []
        for cred in product(self.exploit_user_list, self.exploit_password_list, [''], ['']):
            cred_list.append(cred)
        for cred in product(self.exploit_user_list, [''], [''], self.exploit_ntlm_hash_list):
            cred_list.append(cred)
        for cred in product(self.exploit_user_list, [''], self.exploit_lm_hash_list, ['']):
            cred_list.append(cred)
        return cred_list

    exploit_user_list = ['Administrator', 'root', 'user']
    exploit_password_list = ["Password1!", "1234", "password", "12345678"]
    exploit_lm_hash_list = []
    exploit_ntlm_hash_list = []

    # smb/wmi exploiter
    smb_download_timeout = 300  # timeout in seconds
    smb_service_name = "InfectionMonkey"

    # Timeout (in seconds) for sambacry's trigger to yield results.
    sambacry_trigger_timeout = 5
    # Folder paths to guess share lies inside.
    sambacry_folder_paths_to_guess = ['/', '/mnt', '/tmp', '/storage', '/export', '/share', '/shares', '/home']
    # Shares to not check if they're writable.
    sambacry_shares_not_to_check = ["IPC$", "print$"]

    # system info collection
    collect_system_info = True

    ###########################
    # systeminfo config
    ###########################

    mimikatz_dll_name = "mk.dll"

    extract_azure_creds = True


WormConfiguration = Configuration()
