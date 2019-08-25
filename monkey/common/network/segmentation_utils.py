from common.network.network_range import NetworkRange


def get_ip_in_src_and_not_in_dst(ip_addresses, source_subnet, target_subnet):
    # type: (List[str], NetworkRange, NetworkRange) -> Union[str, None]
    """
    Finds an IP address in ip_addresses which is in source_subnet but not in target_subnet.
    :param ip_addresses:    List of IP addresses to test.
    :param source_subnet:   Subnet to want an IP to not be in.
    :param target_subnet:   Subnet we want an IP to be in.
    :return:    The cross segment IP if in source but not in target, else None.
    """
    for ip_address in ip_addresses:
        if target_subnet.is_in_range(ip_address):
            return None
    for ip_address in ip_addresses:
        if source_subnet.is_in_range(ip_address):
            return ip_address
    return None
