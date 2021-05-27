import os
import stat


def set_perms_to_owner_only(path: str):
    # Read, write, and execute by owner
    os.chmod(path, stat.S_IRWXU)
