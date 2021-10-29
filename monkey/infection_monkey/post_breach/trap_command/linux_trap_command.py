def get_linux_trap_commands():
    return [
        # trap and send SIGTERM signal
        "trap 'echo \"Successfully used trap command\"' TERM && kill -15 $$ ;",
        "trap - TERM",  # untrap SIGTERM
    ]
