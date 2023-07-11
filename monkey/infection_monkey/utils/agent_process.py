import os

import psutil


def get_start_time() -> float:
    agent_process = psutil.Process(os.getpid())
    return agent_process.create_time()
