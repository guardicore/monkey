import datetime


def get_linux_commands_to_add_user(username):
    return [
        'useradd',
        '-M',  # Do not create homedir
        '--expiredate',
        datetime.datetime.today().strftime('%Y-%m-%d'),
        '--inactive',
        '0',
        '-c',  # Comment
        'MONKEY_USER',  # Comment
        username]


def get_linux_commands_to_delete_user(username):
    return [
        'deluser',
        username
    ]
