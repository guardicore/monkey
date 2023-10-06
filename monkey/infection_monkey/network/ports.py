from typing import List

from monkeytypes import NetworkPort

COMMON_PORTS: List[NetworkPort] = [
    NetworkPort(8080),  # http-proxy
    NetworkPort(8008),  # Alternative port for HTTP
    NetworkPort(3389),  # Windows Terminal Server (RDP)
    NetworkPort(1025),  # NFS, IIS
    NetworkPort(3306),  # mysql
    NetworkPort(5985),  # Windows PowerShell Default psSession port
    NetworkPort(5986),  # Windows PowerShell Default psSession port
    NetworkPort(5000),  # A bunch of different stuff (unofficial)
    NetworkPort(5432),  # PostgreSQL
    NetworkPort(1723),  # Microsoft PPTP VPN
    NetworkPort(6600),  # Microsoft Hyper-V Live
    NetworkPort(8888),  # sun-answerbook
    NetworkPort(1433),  # Microsoft SQL Server
    NetworkPort(1434),  # Microsoft SQL Monitor
    NetworkPort(1720),  # h323q931
    NetworkPort(5900),  # vnc
    NetworkPort(6001),  # X11:1
]
