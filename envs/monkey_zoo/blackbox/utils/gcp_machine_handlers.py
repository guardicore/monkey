import logging
import os
import subprocess
from collections.abc import Collection
from threading import Thread

logger = logging.getLogger(__name__)

AUTHENTICATION_COMMAND = "gcloud auth activate-service-account --key-file=%s"
SET_PROPERTY_PROJECT = "gcloud config set project %s"
MACHINE_STARTING_COMMAND = "gcloud compute instances start %s --zone=%s"
MACHINE_STOPPING_COMMAND = "gcloud compute instances stop %s --zone=%s"

# Key path location relative to this file's directory
RELATIVE_KEY_PATH = "../../gcp_keys/gcp_key.json"
DEFAULT_PROJECT = "guardicore-22050661"


def initialize_gcp_client():
    abs_key_path = get_absolute_key_path()

    subprocess.call(get_auth_command(abs_key_path), shell=True)  # noqa: DUO116
    logger.info("GCP Handler passed key")

    subprocess.call(get_set_project_command(DEFAULT_PROJECT), shell=True)  # noqa: DUO116
    logger.info("GCP Handler set project")
    logger.info("GCP Handler initialized successfully")


def get_absolute_key_path() -> str:
    file_dir = os.path.dirname(os.path.realpath(__file__))
    absolute_key_path = os.path.join(file_dir, RELATIVE_KEY_PATH)
    absolute_key_path = os.path.realpath(absolute_key_path)

    if not os.path.isfile(absolute_key_path):
        raise FileNotFoundError(
            "GCP key not found. " "Add a service key to envs/monkey_zoo/gcp_keys/gcp_key.json"
        )
    return absolute_key_path


def start_machines(machine_list: dict[str, Collection[str]]):
    """
    Start all the machines in the list.
    :param machine_list: A dictionary with zone and machines per zone.
    """
    logger.info("Setting up all GCP machines...")
    try:
        run_gcp_command(MACHINE_STARTING_COMMAND, machine_list)
        logger.info("GCP machines successfully started.")
    except Exception as e:
        logger.error("GCP Handler failed to start GCP machines: %s" % e)
        raise e


def stop_machines(machine_list: dict[str, Collection[str]]):
    try:
        run_gcp_command(MACHINE_STOPPING_COMMAND, machine_list)
        logger.info("GCP machines stopped successfully.")
    except Exception as e:
        logger.error("GCP Handler failed to stop network machines: %s" % e)


def get_auth_command(key_path):
    return AUTHENTICATION_COMMAND % key_path


def get_set_project_command(project):
    return SET_PROPERTY_PROJECT % project


def _run_gcp_command(gcp_command: str, machine_list: Collection[str], zone: str):
    """Runs the command in the given zone"""
    ret = subprocess.run(  # noqa DUO116
        (gcp_command % (" ".join(machine_list), zone)),
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        shell=True,
    )
    if ret.returncode != 0:
        raise Exception(f"Failed starting GCP machines: {ret.stderr.decode()}")


def run_gcp_command(gcp_command: str, machine_list: dict[str, Collection[str]]):
    command_threads = [
        Thread(target=_run_gcp_command, args=(gcp_command, machine_list[zone], zone))
        for zone in machine_list
    ]
    for thread in command_threads:
        thread.start()
    for thread in command_threads:
        thread.join()
