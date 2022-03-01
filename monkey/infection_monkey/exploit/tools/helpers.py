import logging

logger = logging.getLogger(__name__)


def try_get_target_monkey(host):
    src_path = get_target_monkey(host)
    if not src_path:
        raise Exception("Can't find suitable monkey executable for host %r", host)
    return src_path


def get_target_monkey(host):
    raise NotImplementedError("get_target_monkey() has been retired. Use IAgentRepository instead.")


def get_target_monkey_by_os(is_windows, is_32bit):
    raise NotImplementedError(
        "get_target_monkey_by_os() has been retired. Use IAgentRepository instead."
    )


def get_monkey_depth():
    from infection_monkey.config import WormConfiguration

    return WormConfiguration.depth


def get_monkey_dest_path(url_to_monkey):
    """
    Gets destination path from monkey's source url.
    :param url_to_monkey: Hosted monkey's url. egz : http://localserver:9999/monkey/windows-64.exe
    :return: Corresponding monkey path from configuration
    """
    from infection_monkey.config import WormConfiguration

    if not url_to_monkey or ("linux" not in url_to_monkey and "windows" not in url_to_monkey):
        logger.error("Can't get destination path because source path %s is invalid.", url_to_monkey)
        return False
    try:
        if "linux" in url_to_monkey:
            return WormConfiguration.dropper_target_path_linux
        elif "windows-64" in url_to_monkey:
            return WormConfiguration.dropper_target_path_win_64
        else:
            logger.error(
                "Could not figure out what type of monkey server was trying to upload, "
                "thus destination path can not be chosen."
            )
            return False
    except AttributeError:
        logger.error(
            "Seems like monkey's source configuration property names changed. "
            "Can not get destination path to upload monkey"
        )
        return False
