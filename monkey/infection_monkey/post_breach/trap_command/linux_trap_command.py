def get_linux_trap_commands():
    return [
        'trap \'echo \"Successfully used trap command\"\' INT && kill -2 $$ ;',  # trap and send SIGINT signal
        'trap - INT'  # untrap SIGINT
    ]
