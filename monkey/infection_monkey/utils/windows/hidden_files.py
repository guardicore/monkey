HIDDEN_FILE = 'C:\\monkey-hidden-file'
HIDDEN_FOLDER = 'C:\\monkey-hidden-folder'


def get_windows_commands_to_hide_files():
    return [
        'echo Successfully created hidden file >',  # create text file
        HIDDEN_FILE,
        '&& attrib',    # change file attributes
        '+h',           # make hidden
        HIDDEN_FILE
    ]


def get_windows_commands_to_hide_folders():
    return [
        'mkdir',        # make directory
        HIDDEN_FOLDER,
        '&& attrib',    # change file attributes
        '+h',           # make hidden
        HIDDEN_FOLDER,
        '&& echo Successfully created hidden folder >'
        '{}\{}'.format(HIDDEN_FOLDER, 'some-file')
    ]


# def get_winAPI_commands_to_hide_files():
#     pass


def get_windows_commands_to_delete():
    return [
        'del',          # delete file
        '/f',           # force delete
        HIDDEN_FILE,
        '&& rmdir',     # delete folder
        HIDDEN_FOLDER
    ]
