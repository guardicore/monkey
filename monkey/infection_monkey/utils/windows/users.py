ACTIVE_NO_NET_USER = '/ACTIVE:NO'


def get_windows_commands_to_add_user(username, password, should_be_active=False):
    windows_cmds = [
        'net',
        'user',
        username,
        password,
        '/add']
    if not should_be_active:
        windows_cmds.append(ACTIVE_NO_NET_USER)
    return windows_cmds


def get_windows_commands_to_delete_user(username):
    return [
        'net',
        'user',
        username,
        '/delete']


def get_windows_commands_to_deactivate_user(username):
    return [
        'net',
        'user',
        username,
        ACTIVE_NO_NET_USER]
