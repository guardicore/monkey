import logging
import os
import subprocess
from typing import List

from monkey_island.cc.server_utils.consts import MONGO_EXECUTABLE_PATH

logger = logging.getLogger(__name__)

DB_DIR_PARAM = "--dbpath"
MONGO_LOG_FILENAME = "mongodb.log"
TERMINATE_TIMEOUT = 10


class MongoDbProcess:
    def __init__(self, db_dir: str, logging_dir: str):
        """
        @param db_dir: Path where a folder for database contents will be created
        @param logging_dir: Path to a folder where mongodb logs will be created
        """
        self._db_dir = db_dir
        self._logging_dir = logging_dir
        self._process = None

    def start(self):
        logger.info("Starting MongoDb process.")

        mongo_run_cmd = MongoDbProcess._build_mongo_run_cmd(MONGO_EXECUTABLE_PATH, self._db_dir)
        logger.info(f"Mongodb will be launched with command: {' '.join(mongo_run_cmd)}.")

        mongo_log_path = os.path.join(self._logging_dir, MONGO_LOG_FILENAME)
        logger.info(f"Mongodb log will be available at {mongo_log_path}.")

        with open(mongo_log_path, "w") as log:
            self._process = subprocess.Popen(mongo_run_cmd, stderr=subprocess.STDOUT, stdout=log)
        logger.info("MongoDb launched successfully!")

    def stop(self):
        if self._process:
            logger.info("Terminating MongoDB process")
            self._process.terminate()
            try:
                self._process.wait(timeout=TERMINATE_TIMEOUT)
                logger.info("MongoDB process terminated successfully")
            except subprocess.TimeoutExpired as te:
                logger.warning(
                    f"MongoDB did not terminate gracefully and will be forcefully killed: {te}"
                )
                self._process.kill()

    @staticmethod
    def _build_mongo_run_cmd(exec_path: str, db_dir: str) -> List[str]:
        return [exec_path, DB_DIR_PARAM, db_dir]
