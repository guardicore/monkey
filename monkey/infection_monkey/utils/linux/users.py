import datetime


def get_linux_commands_to_add_user(username):
    return [
        'adduser',  # https://linux.die.net/man/8/adduser
        '-M',  # Do not create homedir
        '--expiredate',  # The date on which the user account will be disabled.
        datetime.datetime.today().strftime('%Y-%m-%d'),
        '--inactive',  # The number of days after a password expires until the account is permanently disabled.
        '0',  # A value of 0 disables the account as soon as the password has expired
        '-c',  # Comment
        'MONKEY_USER',  # Comment
        username]


def get_linux_commands_to_delete_user(username):
    return [
        'deluser',
        username
    ]
