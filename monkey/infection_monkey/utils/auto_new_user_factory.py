from infection_monkey.utils.environment import is_windows_os
from infection_monkey.utils.linux.users import AutoNewLinuxUser
from infection_monkey.utils.windows.users import AutoNewWindowsUser


def create_auto_new_user(username, password, is_windows=is_windows_os()):
    """
    Factory method for creating an AutoNewUser. See AutoNewUser's documentation for more information.
    Example usage:
        with create_auto_new_user(username, PASSWORD) as new_user:
            ...
    :param username: The username of the new user.
    :param password: The password of the new user.
    :param is_windows: If True, a new Windows user is created. Otherwise, a Linux user is created. Leave blank for
    automatic detection.
    :return: The new AutoNewUser object - use with a `with` scope.
    """
    if is_windows:
        return AutoNewWindowsUser(username, password)
    else:
        return AutoNewLinuxUser(username, password)
