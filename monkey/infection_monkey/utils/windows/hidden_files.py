HIDDEN_FILE = "%temp%\\monkey-hidden-file"
HIDDEN_FILE_WINAPI = "%temp%\\monkey-hidden-file-winAPI"
HIDDEN_FOLDER = "%temp%\\monkey-hidden-folder"


def get_windows_commands_to_hide_files():
    return [
        'echo',
        'Successfully created hidden file: {}'.format(HIDDEN_FILE),  # create empty file
        '>',
        HIDDEN_FILE,
        '&&',
        'attrib',       # change file attributes
        '+h',           # make hidden
        HIDDEN_FILE,
        '&&',
        'type',
        HIDDEN_FILE
    ]


def get_windows_commands_to_hide_folders():
    return [
        'mkdir',
        HIDDEN_FOLDER,  # make directory
        '&&',
        'attrib',
        '+h',
        HIDDEN_FOLDER,  # change file attributes
        '&&',
        'echo',
        'Successfully created hidden folder: {}'.format(HIDDEN_FOLDER),
        '>',
        '{}\\{}'.format(HIDDEN_FOLDER, 'some-file'),
        '&&',
        'type',
        '{}\\{}'.format(HIDDEN_FOLDER, 'some-file')
    ]


def get_winAPI_to_hide_files():
    import win32file
    try:
        fileAccess = win32file.GENERIC_READ | win32file.GENERIC_WRITE  # read-write access
        fileCreation = win32file.CREATE_ALWAYS  # overwrite existing file
        fileFlags = win32file.FILE_ATTRIBUTE_HIDDEN  # make hidden

        hiddenFile = win32file.CreateFile(HIDDEN_FILE_WINAPI,
                                          fileAccess,
                                          0,  # sharing mode: 0 => can't be shared
                                          None,  # security attributes
                                          fileCreation,
                                          fileFlags,
                                          0)  # template file

        return "Succesfully created hidden file: {}".format(HIDDEN_FILE_WINAPI), True
    except Exception as err:
        return str(err), False


def get_windows_commands_to_delete():
    return [
        'del',          # delete file
        '-Force',           # force delete
        HIDDEN_FILE,
        HIDDEN_FILE_WINAPI,
        '&&',
        'rmdir',     # delete folder
        '-Force',
        HIDDEN_FOLDER
    ]
