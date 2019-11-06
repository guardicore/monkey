import filecmp
import shutil
import os
import logging

from infection_monkey.config import WormConfiguration


LOG = logging.getLogger(__name__)


class FileMover:

    @staticmethod
    def move_file(source_path, destination_path):
        # we copy/move only in case path is different
        need_to_move = not FileMover.is_same_path(source_path, destination_path)

        if need_to_move and os.path.exists(destination_path):
            os.remove(destination_path)

        # first try to move the file
        if need_to_move and WormConfiguration.dropper_try_move_first:
            need_to_move = not FileMover.try_move_to_dst(source_path, destination_path)

        # if file still need to change path, copy it
        if need_to_move:
            need_to_move = not FileMover.try_copy_to_dst(source_path, destination_path)

        return not need_to_move

    @staticmethod
    def is_same_path(path1, path2):
        try:
            return filecmp.cmp(path1, path2)
        except OSError:
            return False

    @staticmethod
    def try_move_to_dst(source_path, destination_path):
        try:
            shutil.move(source_path,
                        destination_path)
            LOG.info("Moved source file '%s' into '%s'", source_path, destination_path)
            return True
        except (WindowsError, IOError, OSError) as exc:
            LOG.debug("Error moving source file '%s' into '%s': %s", source_path, destination_path, exc)
            return False

    @staticmethod
    def try_copy_to_dst(source_path, destination_path):
        try:
            shutil.copy(source_path, destination_path)

            LOG.info("Copied source file '%s' into '%s'", source_path, destination_path)
        except (WindowsError, IOError, OSError) as exc:
            LOG.error("Error copying source file '%s' into '%s': %s", source_path, destination_path, exc)
            return False
