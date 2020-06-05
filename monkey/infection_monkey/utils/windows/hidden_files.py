HIDDEN_FILE = 'C:\\monkey-hidden-file'
HIDDEN_FILE_WINAPI = 'C:\\monkey-hidden-file-winAPI'
HIDDEN_FOLDER = 'C:\\monkey-hidden-folder'


def get_windows_commands_to_hide_files():
    return [
        'type NUL >',   # create empty file
        HIDDEN_FILE,
        '&& attrib',    # change file attributes
        '+h',           # make hidden
        HIDDEN_FILE,
        'echo Successfully created hidden file: {0} > {0}'.format(HIDDEN_FILE),
        '&& type {}'.format(HIDDEN_FILE)
    ]


def get_windows_commands_to_hide_folders():
    return [
        'mkdir',        # make directory
        HIDDEN_FOLDER,
        '&& attrib',    # change file attributes
        '+h',           # make hidden
        HIDDEN_FOLDER,
        '&& echo Successfully created hidden folder: {} >'.format(HIDDEN_FOLDER),
        '{}\\{}'.format(HIDDEN_FOLDER, 'some-file'),
        '&& type {}'.format(HIDDEN_FOLDER, 'some-file')
    ]


def get_winAPI_to_hide_files():
    import win32file
    try:
        fileAccess = win32file.GENERIC_READ | win32file.GENERIC_WRITE  # read-write access
        fileCreation = win32file.CREATE_ALWAYS  # overwrite existing file
        fileFlags = win32file.FILE_ATTRIBUTE_HIDDEN  # make hidden

        hiddenFile = win32file.CreateFile(HIDDEN_FILE_WINAPI,
                                          fileAccess,
                                          0,
                                          None,
                                          fileCreation,
                                          fileFlags,
                                          0)

        return "Succesfully created hidden file: {}".format(HIDDEN_FILE_WINAPI), True
    except Exception as err:
        return str(err), False


def get_windows_commands_to_delete():
    return [
        'del',          # delete file
        '/f',           # force delete
        HIDDEN_FILE,
        HIDDEN_FILE_WINAPI,
        '&& rmdir',     # delete folder
        HIDDEN_FOLDER
    ]
