import logging

LOG = logging.getLogger(__name__)


def try_get_target_monkey(host):
    src_path = get_target_monkey(host)
    if not src_path:
        raise Exception("Can't find suitable monkey executable for host %r", host)
    return src_path


def get_target_monkey(host):
    import platform
    import sys

    from infection_monkey.control import ControlClient

    if host.monkey_exe:
        return host.monkey_exe

    if not host.os.get('type'):
        return None

    monkey_path = ControlClient.download_monkey_exe(host)

    if host.os.get('machine') and monkey_path:
        host.monkey_exe = monkey_path

    if not monkey_path:
        if host.os.get('type') == platform.system().lower():
            # if exe not found, and we have the same arch or arch is unknown and we are 32bit, use our exe
            if (not host.os.get('machine') and sys.maxsize < 2 ** 32) or \
                    host.os.get('machine', '').lower() == platform.machine().lower():
                monkey_path = sys.executable

    return monkey_path


def get_target_monkey_by_os(is_windows, is_32bit):
    from infection_monkey.control import ControlClient
    return ControlClient.download_monkey_exe_by_os(is_windows, is_32bit)


def build_monkey_commandline_explicitly(parent=None, tunnel=None, server=None, depth=None, location=None,
                                        vulnerable_port=None):
    cmdline = ""

    if parent is not None:
        cmdline += f" -p {parent}"
    if tunnel is not None:
        cmdline += f" -t {tunnel}"
    if server is not None:
        cmdline += f" -s {server}"
    if depth is not None:
        if int(depth) < 0:
            depth = 0
        cmdline += f" -d {depth}"
    if location is not None:
        cmdline += f" -l {location}"
    if vulnerable_port is not None:
        cmdline += f" -vp {vulnerable_port}"

    return cmdline


def build_monkey_commandline(target_host, depth, vulnerable_port, location=None):
    from infection_monkey.config import GUID
    return build_monkey_commandline_explicitly(
        GUID, target_host.default_tunnel, target_host.default_server, depth, location, vulnerable_port)


def get_monkey_depth():
    from infection_monkey.config import WormConfiguration
    return WormConfiguration.depth


def get_monkey_dest_path(url_to_monkey):
    """
    Gets destination path from monkey's source url.
    :param url_to_monkey: Hosted monkey's url. egz : http://localserver:9999/monkey/windows-32.exe
    :return: Corresponding monkey path from configuration
    """
    from infection_monkey.config import WormConfiguration
    if not url_to_monkey or ('linux' not in url_to_monkey and 'windows' not in url_to_monkey):
        LOG.error("Can't get destination path because source path %s is invalid.", url_to_monkey)
        return False
    try:
        if 'linux' in url_to_monkey:
            return WormConfiguration.dropper_target_path_linux
        elif 'windows-32' in url_to_monkey:
            return WormConfiguration.dropper_target_path_win_32
        elif 'windows-64' in url_to_monkey:
            return WormConfiguration.dropper_target_path_win_64
        else:
            LOG.error("Could not figure out what type of monkey server was trying to upload, "
                      "thus destination path can not be chosen.")
            return False
    except AttributeError:
        LOG.error("Seems like monkey's source configuration property names changed. "
                  "Can not get destination path to upload monkey")
        return False
