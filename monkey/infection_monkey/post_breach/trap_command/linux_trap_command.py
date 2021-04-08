def get_linux_trap_commands():
    return [
        # trap and send SIGINT signal
        "trap 'echo \"Successfully used trap command\"' INT && kill -2 $$ ;",
        "trap - INT",  # untrap SIGINT
    ]
