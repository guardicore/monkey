from typing import List

COMMON_PORTS: List[int] = [
    1025,  # NFS, IIS
    1433,  # Microsoft SQL Server
    1434,  # Microsoft SQL Monitor
    1720,  # h323q931
    1723,  # Microsoft PPTP VPN
    3306,  # mysql
    3389,  # Windows Terminal Server (RDP)
    5900,  # vnc
    6001,  # X11:1
    8080,  # http-proxy
    8888,  # sun-answerbook
]
