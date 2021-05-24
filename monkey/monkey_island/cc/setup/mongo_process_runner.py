import logging
import os
import subprocess
from typing import List

from monkey_island.cc.server_utils.common_methods import WINDOWS, get_runtime_os
from monkey_island.cc.server_utils.consts import (
    MONGO_EXECUTABLE_PATH_LINUX,
    MONGO_EXECUTABLE_PATH_WIN,
)

logger = logging.getLogger(__name__)

DB_DIR_NAME = "db"
DB_DIR_PARAM = "--dbpath"
MONGO_LOG_FILENAME = "mongo_log.txt"


class MongoDbRunner:
    def __init__(self, db_dir_parent_path: str, logging_dir_path: str):
        """
        @param db_dir_parent_path: Path where a folder for database contents will be created
        @param logging_dir_path: Path to a folder where mongodb logs will be created
        """
        self.db_dir_parent_path = db_dir_parent_path
        self.logging_dir_path = logging_dir_path

    def launch_mongodb(self):
        db_path = self._create_db_dir()
        self._start_mongodb_process(db_path)

    def _create_db_dir(self) -> str:
        db_path = os.path.join(self.db_dir_parent_path, DB_DIR_NAME)
        logger.info(f"Database content directory: {db_path}.")
        if not os.path.isdir(db_path):
            logger.info("Database content directory not found, creating one.")
            os.mkdir(os.path.join(self.db_dir_parent_path, DB_DIR_NAME))
        return db_path

    def _start_mongodb_process(self, db_dir_path: str):
        logger.info("Starting MongoDb process.")
        mongo_exec = MongoDbRunner._get_path_of_mongo_exec()

        mongo_run_cmd = MongoDbRunner._build_mongo_launch_cmd(mongo_exec, db_dir_path)
        logger.info(f"Mongodb will be launched with command: f{' '.join(mongo_run_cmd)}.")

        mongo_log_path = os.path.join(self.logging_dir_path, MONGO_LOG_FILENAME)
        logger.info(f"Mongodb log will be available at f{mongo_log_path}.")

        with open(mongo_log_path, "w") as log:
            subprocess.Popen(mongo_run_cmd, stderr=subprocess.STDOUT, stdout=log)
        logger.info("MongoDb launched successfully!")

    @staticmethod
    def _get_path_of_mongo_exec():
        if get_runtime_os() == WINDOWS:
            return MONGO_EXECUTABLE_PATH_WIN
        else:
            return MONGO_EXECUTABLE_PATH_LINUX

    @staticmethod
    def _build_mongo_launch_cmd(exec_path: str, db_path: str) -> List[str]:
        return [exec_path, DB_DIR_PARAM, db_path]
