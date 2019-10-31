def get_ip_in_src_and_not_in_dst(ip_addresses, source_subnet, target_subnet):
    """
    Finds an IP address in ip_addresses which is in source_subnet but not in target_subnet.
    :param ip_addresses:    List[str]: List of IP addresses to test.
    :param source_subnet:   NetworkRange: Subnet to want an IP to not be in.
    :param target_subnet:   NetworkRange: Subnet we want an IP to be in.
    :return:    The cross segment IP if in source but not in target, else None. Union[str, None]
    """
    if get_ip_if_in_subnet(ip_addresses, target_subnet) is not None:
        return None
    return get_ip_if_in_subnet(ip_addresses, source_subnet)


def get_ip_if_in_subnet(ip_addresses, subnet):
    """
    :param ip_addresses: IP address list.
    :param subnet: Subnet to check if one of ip_addresses is in there. This is common.network.network_range.NetworkRange
    :return: The first IP in ip_addresses which is in the subnet if there is one, otherwise returns None.
    """
    for ip_address in ip_addresses:
        if subnet.is_in_range(ip_address):
            return ip_address
    return None
