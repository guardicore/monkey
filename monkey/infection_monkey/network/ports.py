from typing import List

COMMON_PORTS: List[int] = [
    8080,  # http-proxy
    8008,  # Alternative port for HTTP
    3389,  # Windows Terminal Server (RDP)
    1025,  # NFS, IIS
    3306,  # mysql
    5985,  # Windows PowerShell Default psSession port
    5986,  # Windows PowerShell Default psSession port
    5000,  # A bunch of different stuff (unofficial)
    5432,  # PostgreSQL
    1723,  # Microsoft PPTP VPN
    6600,  # Microsoft Hyper-V Live
    8888,  # sun-answerbook
    1433,  # Microsoft SQL Server
    1434,  # Microsoft SQL Monitor
    1720,  # h323q931
    5900,  # vnc
    6001,  # X11:1
]
