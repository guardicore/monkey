def get_windows_commands_to_add_user(username, password, should_be_active=False):
    windows_cmds = [
        'net',
        'user',
        username,
        password,
        '/add']
    if not should_be_active:
        windows_cmds.append('/ACTIVE:NO')
    return windows_cmds


def get_windows_commands_to_delete_user(username):
    return [
        'net',
        'user',
        username,
        '/delete']
