import os
from io import BytesIO

__author__ = 'hoffer'

MONKEYFS_PREFIX = 'monkeyfs://'

open_orig = open


class VirtualFile(BytesIO):
    _vfs = {}  # virtual File-System

    def __init__(self, name, mode='r', buffering=None):
        if not name.startswith(MONKEYFS_PREFIX):
            name = MONKEYFS_PREFIX + name
        self.name = name
        self._mode = mode
        if name in VirtualFile._vfs:
            super(VirtualFile, self).__init__(self._vfs[name])
        else:
            super(VirtualFile, self).__init__()

    def flush(self):
        super(VirtualFile, self).flush()
        VirtualFile._vfs[self.name] = self.getvalue()

    @staticmethod
    def getsize(path):
        return len(VirtualFile._vfs[path])

    @staticmethod
    def isfile(path):
        return path in VirtualFile._vfs


def getsize(path):
    if path.startswith(MONKEYFS_PREFIX):
        return VirtualFile.getsize(path)
    else:
        return os.stat(path).st_size


def isfile(path):
    if path.startswith(MONKEYFS_PREFIX):
        return VirtualFile.isfile(path)
    else:
        return os.path.isfile(path)


def virtual_path(name):
    return "%s%s" % (MONKEYFS_PREFIX, name)


# noinspection PyShadowingBuiltins
def open(name, mode='r', buffering=-1):
    # use normal open for regular paths, and our "virtual" open for monkeyfs:// paths
    if name.startswith(MONKEYFS_PREFIX):
        return VirtualFile(name, mode, buffering)
    else:
        return open_orig(name, mode=mode, buffering=buffering)
