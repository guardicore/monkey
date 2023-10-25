import atexit
import os
from pathlib import Path

from monkey_island.cc.setup.nextjs.nextjs_process import NextJsProcess

NEXTJS_LOG_FILENAME = "nextjs.log"


def start_nextjs(data_dir: Path) -> NextJsProcess:
    log_file = os.path.join(data_dir, NEXTJS_LOG_FILENAME)

    nextjs_process = NextJsProcess(log_file=log_file)
    nextjs_process.start()

    return nextjs_process


def register_nextjs_shutdown_callback(nextjs_process: NextJsProcess):
    atexit.register(nextjs_process.stop)
