MONKEY_ARG = "m0nk3y"
DROPPER_ARG = "dr0pp3r"

SET_OTP_WINDOWS = "set %(agent_otp_environment_variable)s=%(agent_otp)s&"

# CMD prefix for windows commands
CMD_EXE = "cmd.exe"
CMD_CARRY_OUT = "/c"
CMD_PREFIX = CMD_EXE + " " + CMD_CARRY_OUT

RUN_MONKEY = "%(monkey_path)s %(monkey_type)s %(parameters)s"
