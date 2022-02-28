import hashlib
import json
import logging
import os

import flask_restful
from flask import request, send_from_directory

from monkey_island.cc.server_utils.consts import MONKEY_ISLAND_ABS_PATH

logger = logging.getLogger(__name__)

MONKEY_DOWNLOADS = [
    {
        "type": "linux",
        "filename": "monkey-linux-64",
    },
    {
        "type": "windows",
        "filename": "monkey-windows-64.exe",
    },
]


def get_monkey_executable(host_os):
    for download in MONKEY_DOWNLOADS:
        if host_os == download.get("type"):
            logger.info(f"Monkey exec found for os: {host_os}")
            return download
    logger.warning(f"No monkey executables could be found for the host os: {host_os}")
    return None


class MonkeyDownload(flask_restful.Resource):

    # Used by monkey. can't secure.
    def get(self, path):
        return send_from_directory(os.path.join(MONKEY_ISLAND_ABS_PATH, "cc", "binaries"), path)

    # Used by monkey. can't secure.
    def post(self):
        host_json = json.loads(request.data)
        host_os = host_json.get("os")
        if host_os:
            result = get_monkey_executable(host_os.get("type"))

            if result:
                # change resulting from new base path
                executable_filename = result["filename"]
                real_path = MonkeyDownload.get_executable_full_path(executable_filename)
                if os.path.isfile(real_path):
                    result["size"] = os.path.getsize(real_path)
                    return result

        return {}

    @staticmethod
    def get_executable_full_path(executable_filename):
        real_path = os.path.join(MONKEY_ISLAND_ABS_PATH, "cc", "binaries", executable_filename)
        return real_path

    @staticmethod
    def log_executable_hashes():
        """
        Logs all the hashes of the monkey executables for debugging ease (can check what Monkey
        version you have etc.).
        """
        filenames = set([x["filename"] for x in MONKEY_DOWNLOADS])
        for filename in filenames:
            filepath = MonkeyDownload.get_executable_full_path(filename)
            if os.path.isfile(filepath):
                with open(filepath, "rb") as monkey_exec_file:
                    file_contents = monkey_exec_file.read()
                    logger.debug(
                        "{} hashes:\nSHA-256 {}".format(
                            filename, hashlib.sha256(file_contents).hexdigest()
                        )
                    )
            else:
                logger.debug("No monkey executable for {}.".format(filepath))
