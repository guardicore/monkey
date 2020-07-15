import socket

DEFAULT_TIMEOUT = 5  # Seconds


def check_tcp_port(ip: str, port: str, timeout=DEFAULT_TIMEOUT) -> bool:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

    try:
        sock.connect((ip, int(port)))
    except socket.timeout:
        return False
    except socket.error:
        return False
    finally:
        sock.close()
    return True
