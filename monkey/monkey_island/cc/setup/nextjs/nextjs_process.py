import logging
import subprocess

from monkey_island.cc.server_utils.consts import NEXTJS_EXECUTION_COMMAND, UI_DIR

TERMINATE_TIMEOUT = 10
logger = logging.getLogger(__name__)


class NextJsProcess:
    def __init__(self, log_file: str):
        """
        @param log_file: Path to the file that will contain nextjs logs
        """
        self._next_js_run_cmd = NEXTJS_EXECUTION_COMMAND
        self._log_file = log_file
        self._process = None

    def start(self):
        logger.info("Starting UI server(Next.js) process.")
        logger.debug(
            f"Next.js server will be launched with command: {' '.join(self._next_js_run_cmd)}"
        )
        logger.info(f"UI log will be available at {self._log_file}.")

        with open(self._log_file, "w") as log:
            self._process = subprocess.Popen(
                self._next_js_run_cmd, cwd=UI_DIR, stderr=subprocess.STDOUT, stdout=log
            )

        logger.info("UI server(Next.js) has been started!")

    def stop(self):
        if not self._process:
            logger.warning("Failed to stop Next.js process: No process found")
            return

        logger.info("Terminating UI server(Next.js)")
        self._process.terminate()

        try:
            self._process.wait(timeout=TERMINATE_TIMEOUT)
            logger.info("UI server(Next.js) terminated successfully")
        except subprocess.TimeoutExpired as te:
            logger.warning(
                f"UI server(Next.js) did not terminate gracefully "
                f"and will be forcefully killed: {te}"
            )
            self._process.kill()