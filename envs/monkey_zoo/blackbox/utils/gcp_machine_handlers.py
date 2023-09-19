import logging
import os
import subprocess
from multiprocessing.dummy import Pool

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


def start_machines(machine_list):
    """
    Start all the machines in the list.
    :param machine_list: A dictionary with zone and machines per zone.
    """
    logger.info("Setting up all GCP machines...")
    try:
        run_gcp_pool(MACHINE_STARTING_COMMAND, machine_list)
        logger.info("GCP machines successfully started.")
    except Exception as e:
        logger.error("GCP Handler failed to start GCP machines: %s" % e)
        raise e


def stop_machines(machine_list):
    try:
        run_gcp_pool(MACHINE_STOPPING_COMMAND, machine_list)
        logger.info("GCP machines stopped successfully.")
    except Exception as e:
        logger.error("GCP Handler failed to stop network machines: %s" % e)


def get_auth_command(key_path):
    return AUTHENTICATION_COMMAND % key_path


def get_set_project_command(project):
    return SET_PROPERTY_PROJECT % project


def run_gcp_command(arglist):
    gcp_cmd, machine_list, zone = arglist
    ret = subprocess.run(  # noqa DUO116
        (gcp_cmd % (" ".join(machine_list), zone)),
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        shell=True,
    )
    if ret.returncode != 0:
        raise Exception(f"Failed starting GCP machines: {ret.stderr}")


def run_gcp_pool(gcp_command, machine_list):
    arglist = [(gcp_command, machine_list[zone], zone) for zone in machine_list]
    with Pool(2) as pool:
        pool.map(run_gcp_command, arglist)
