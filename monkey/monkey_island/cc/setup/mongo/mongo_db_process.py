import logging
import subprocess

from monkey_island.cc.server_utils.consts import MONGO_EXECUTABLE_PATH

logger = logging.getLogger(__name__)

DB_DIR_PARAM = "--dbpath"
TERMINATE_TIMEOUT = 10


class MongoDbProcess:
    def __init__(self, db_dir: str, log_file: str):
        """
        @param db_dir: Path where a folder for database contents will be created
        @param log_file: Path to the file that will contain mongodb logs
        """
        self._mongo_run_cmd = [MONGO_EXECUTABLE_PATH, DB_DIR_PARAM, db_dir]
        self._log_file = log_file
        self._process = None

    def start(self):
        logger.info("Starting MongoDB process.")
        logger.debug(f"MongoDB will be launched with command: {' '.join(self._mongo_run_cmd)}.")
        logger.info(f"MongoDB log will be available at {self._log_file}.")

        with open(self._log_file, "w") as log:
            self._process = subprocess.Popen(
                self._mongo_run_cmd, stderr=subprocess.STDOUT, stdout=log
            )

        logger.info("MongoDB has been launched!")

    def stop(self):
        if not self._process:
            logger.warning("Failed to stop MongoDB process: No process found")
            return

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

    def is_running(self) -> bool:
        if self._process and self._process.poll() is None:
            return True

        return False

    @property
    def log_file(self) -> str:
        return self._log_file
