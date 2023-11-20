import logging
import os
import subprocess
from typing import Optional

from common.types import NetworkPort
from common.utils.environment import is_windows_os
from monkey_island.cc.server_utils.consts import MONKEY_ISLAND_ABS_PATH

TERMINATE_TIMEOUT = 10
logger = logging.getLogger(__name__)


UI_DIR = os.path.join(MONKEY_ISLAND_ABS_PATH, "cc", "next_ui")
_NODE_EXECUTABLE_PATH_WIN = os.path.join(MONKEY_ISLAND_ABS_PATH, "bin", "node", "node.exe")
_NODE_EXECUTABLE_PATH_LINUX = os.path.join(MONKEY_ISLAND_ABS_PATH, "bin", "node", "node")
NODE_EXECUTABLE_PATH = _NODE_EXECUTABLE_PATH_WIN if is_windows_os() else _NODE_EXECUTABLE_PATH_LINUX
NEXTJS_EXECUTION_COMMAND = [NODE_EXECUTABLE_PATH, "server.js"]


class NextJsProcess:
    def __init__(self, log_file: str, port: NetworkPort, ssl_cert_path: str, ssl_key_path: str):
        """
        @param log_file: Path to the file that will contain nextjs logs
        """
        self._next_js_run_cmd = NEXTJS_EXECUTION_COMMAND
        self._log_file = log_file
        self._port = port
        self._ssl_cert_path = ssl_cert_path
        self._ssl_key_path = ssl_key_path
        self._process: Optional[subprocess.Popen[bytes]] = None

    def start(self):
        logger.info("Starting UI server(Next.js) process.")
        logger.debug(
            f"Next.js server will be launched with command: {' '.join(self._next_js_run_cmd)}"
        )
        logger.info(f"UI log will be available at {self._log_file}.")

        with open(self._log_file, "w") as log:
            node_env = os.environ.copy()
            node_env["JAVASCRIPT_RUNTIME_PORT"] = str(self._port)
            node_env["SSL_CERT_PATH"] = self._ssl_cert_path
            node_env["SSL_KEY_PATH"] = self._ssl_key_path
            self._process = subprocess.Popen(
                self._next_js_run_cmd,
                cwd=UI_DIR,
                stderr=subprocess.STDOUT,
                stdout=log,
                env=node_env,
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
