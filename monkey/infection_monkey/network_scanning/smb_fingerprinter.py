import logging
import socket
import struct
from typing import Dict, List

from odict import odict

from common import OperatingSystem
from common.types import DiscoveredService, NetworkPort, NetworkProtocol, NetworkService, PortStatus
from infection_monkey.i_puppet import FingerprintData, IFingerprinter, PingScanData, PortScanData

SMB_PORT = NetworkPort(445)

logger = logging.getLogger(__name__)


class Packet:
    fields = odict(
        [
            ("data", ""),
        ]
    )

    def __init__(self, **kw):
        self.fields = odict(self.__class__.fields)
        for k, v in list(kw.items()):
            if callable(v):
                self.fields[k] = v(self.fields[k])
            else:
                self.fields[k] = v

    def to_byte_string(self):
        content_list = [
            (x.to_byte_string() if hasattr(x, "to_byte_string") else x)
            for x in self.fields.values()
        ]
        return b"".join(content_list)


# SMB Packets
class SMBHeader(Packet):
    fields = odict(
        [
            ("proto", b"\xff\x53\x4d\x42"),
            ("cmd", b"\x72"),
            ("errorcode", b"\x00\x00\x00\x00"),
            ("flag1", b"\x00"),
            ("flag2", b"\x00\x00"),
            ("pidhigh", b"\x00\x00"),
            ("signature", b"\x00\x00\x00\x00\x00\x00\x00\x00"),
            ("reserved", b"\x00\x00"),
            ("tid", b"\x00\x00"),
            ("pid", b"\x00\x00"),
            ("uid", b"\x00\x00"),
            ("mid", b"\x00\x00"),
        ]
    )


class SMBNego(Packet):
    fields = odict([("wordcount", b"\x00"), ("bcc", b"\x62\x00"), ("data", "")])

    def calculate(self):
        self.fields["bcc"] = struct.pack("<h", len(self.fields["data"].to_byte_string()))


class SMBNegoFingerprintData(Packet):
    fields = odict(
        [
            ("separator1", b"\x02"),
            (
                "dialect1",
                b"\x50\x43\x20\x4e\x45\x54\x57\x4f\x52\x4b\x20\x50\x52\x4f\x47\x52\x41\x4d"
                b"\x20\x31\x2e\x30\x00",
            ),
            ("separator2", b"\x02"),
            ("dialect2", b"\x4c\x41\x4e\x4d\x41\x4e\x31\x2e\x30\x00"),
            ("separator3", b"\x02"),
            (
                "dialect3",
                b"\x57\x69\x6e\x64\x6f\x77\x73\x20\x66\x6f\x72\x20\x57\x6f\x72\x6b\x67\x72"
                b"\x6f\x75\x70\x73\x20\x33\x2e\x31\x61\x00",
            ),
            ("separator4", b"\x02"),
            ("dialect4", b"\x4c\x4d\x31\x2e\x32\x58\x30\x30\x32\x00"),
            ("separator5", b"\x02"),
            ("dialect5", b"\x4c\x41\x4e\x4d\x41\x4e\x32\x2e\x31\x00"),
            ("separator6", b"\x02"),
            ("dialect6", b"\x4e\x54\x20\x4c\x4d\x20\x30\x2e\x31\x32\x00"),
        ]
    )


class SMBSessionFingerprintData(Packet):
    fields = odict(
        [
            ("wordcount", b"\x0c"),
            ("AndXCommand", b"\xff"),
            ("reserved", b"\x00"),
            ("andxoffset", b"\x00\x00"),
            ("maxbuff", b"\x04\x11"),
            ("maxmpx", b"\x32\x00"),
            ("vcnum", b"\x00\x00"),
            ("sessionkey", b"\x00\x00\x00\x00"),
            ("securitybloblength", b"\x4a\x00"),
            ("reserved2", b"\x00\x00\x00\x00"),
            ("capabilities", b"\xd4\x00\x00\xa0"),
            ("bcc1", ""),
            (
                "Data",
                b"\x60\x48\x06\x06\x2b\x06\x01\x05\x05\x02\xa0\x3e\x30\x3c\xa0\x0e\x30\x0c"
                b"\x06\x0a\x2b\x06\x01\x04\x01\x82\x37\x02"
                b"\x02\x0a\xa2\x2a\x04\x28\x4e\x54\x4c\x4d\x53\x53\x50\x00\x01\x00\x00\x00"
                b"\x07\x82\x08\xa2\x00\x00\x00\x00\x00\x00"
                b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\x01\x28\x0a\x00\x00\x00\x0f"
                b"\x00\x57\x00\x69\x00\x6e\x00\x64\x00\x6f"
                b"\x00\x77\x00\x73\x00\x20\x00\x32\x00\x30\x00\x30\x00\x32\x00\x20\x00\x53"
                b"\x00\x65\x00\x72\x00\x76\x00\x69\x00\x63"
                b"\x00\x65\x00\x20\x00\x50\x00\x61\x00\x63\x00\x6b\x00\x20\x00\x33\x00\x20"
                b"\x00\x32\x00\x36\x00\x30\x00\x30\x00\x00"
                b"\x00\x57\x00\x69\x00\x6e\x00\x64\x00\x6f\x00\x77\x00\x73\x00\x20\x00\x32"
                b"\x00\x30\x00\x30\x00\x32\x00\x20\x00\x35"
                b"\x00\x2e\x00\x31\x00\x00\x00\x00\x00",
            ),
        ]
    )

    def calculate(self):
        self.fields["bcc1"] = struct.pack("<i", len(self.fields["Data"]))[:2]


class SMBFingerprinter(IFingerprinter):
    def get_host_fingerprint(
        self,
        host: str,
        _ping_scan_data: PingScanData,
        port_scan_data: Dict[int, PortScanData],
        _options: Dict,
    ) -> FingerprintData:
        services: List[DiscoveredService] = []
        os_type = None
        os_version = None

        if (SMB_PORT not in port_scan_data) or (port_scan_data[SMB_PORT].status != PortStatus.OPEN):
            return FingerprintData(os_type=None, os_version=None, services=services)

        logger.debug(f"Fingerprinting potential SMB port {SMB_PORT} on {host}")

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.7)
            s.connect((host, SMB_PORT))

            h = SMBHeader(cmd=b"\x72", flag1=b"\x18", flag2=b"\x53\xc8")
            n = SMBNego(data=SMBNegoFingerprintData())
            n.calculate()

            packet_ = h.to_byte_string() + n.to_byte_string()
            buffer = struct.pack(">i", len(packet_)) + packet_
            s.send(buffer)
            data = s.recv(2048)

            if data[8:10] == b"\x72\x00":
                header = SMBHeader(cmd=b"\x73", flag1=b"\x18", flag2=b"\x17\xc8", uid=b"\x00\x00")
                body = SMBSessionFingerprintData()
                body.calculate()

                packet_ = header.to_byte_string() + body.to_byte_string()
                buffer = struct.pack(">i", len(packet_)) + packet_

                s.send(buffer)
                data = s.recv(2048)

            if data[8:10] == b"\x73\x16":
                length = struct.unpack("<H", data[43:45])[0]
                os_version, service_client = tuple(
                    [
                        e.replace(b"\x00", b"").decode()
                        for e in data[47 + length :].split(b"\x00\x00\x00")[:2]
                    ]
                )

                logger.debug(f'os_version: "{os_version}", service_client: "{service_client}"')

                if os_version.lower() != "unix":
                    os_type = OperatingSystem.WINDOWS
                else:
                    os_type = OperatingSystem.LINUX

            services.append(
                DiscoveredService(
                    protocol=NetworkProtocol.TCP,
                    port=SMB_PORT,
                    service=NetworkService.SMB,
                )
            )
        except Exception as exc:
            logger.debug("Error getting smb fingerprint: %s", exc)

        return FingerprintData(os_type=os_type, os_version=os_version, services=services)
