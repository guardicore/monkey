import logging
import os
import subprocess

LOGGER = logging.getLogger(__name__)


class GCPHandler(object):
    AUTHENTICATION_COMMAND = "gcloud auth activate-service-account --key-file=%s"
    SET_PROPERTY_PROJECT = "gcloud config set project %s"
    MACHINE_STARTING_COMMAND = "gcloud compute instances start %s --zone=%s"
    MACHINE_STOPPING_COMMAND = "gcloud compute instances stop %s --zone=%s"

    # Key path location relative to this file's directory
    RELATIVE_KEY_PATH = "../../gcp_keys/gcp_key.json"
    DEFAULT_PROJECT = "guardicore-22050661"

    def __init__(
        self,
        project_id=DEFAULT_PROJECT,
    ):
        abs_key_path = GCPHandler.get_absolute_key_path()

        subprocess.call(GCPHandler.get_auth_command(abs_key_path), shell=True)  # noqa: DUO116
        LOGGER.info("GCP Handler passed key")

        subprocess.call(GCPHandler.get_set_project_command(project_id), shell=True)  # noqa: DUO116
        LOGGER.info("GCP Handler set project")
        LOGGER.info("GCP Handler initialized successfully")

    @staticmethod
    def get_absolute_key_path() -> str:
        file_dir = os.path.dirname(os.path.realpath(__file__))
        absolute_key_path = os.path.join(file_dir, GCPHandler.RELATIVE_KEY_PATH)
        absolute_key_path = os.path.realpath(absolute_key_path)

        if not os.path.isfile(absolute_key_path):
            raise FileNotFoundError(
                "GCP key not found. " "Add a service key to envs/monkey_zoo/gcp_keys/gcp_key.json"
            )
        return absolute_key_path

    @staticmethod
    def start_machines(machine_list):
        """
        Start all the machines in the list.
        :param machine_list: A dictionary with zone and machines per zone.
        """
        LOGGER.info("Setting up all GCP machines...")
        try:
            for zone in machine_list:
                subprocess.call(  # noqa: DUO116
                    (GCPHandler.MACHINE_STARTING_COMMAND % (" ".join(machine_list[zone]), zone)),
                    shell=True,
                )
            LOGGER.info("GCP machines successfully started.")
        except Exception as e:
            LOGGER.error("GCP Handler failed to start GCP machines: %s" % e)

    @staticmethod
    def stop_machines(machine_list):
        try:
            for zone in machine_list:
                subprocess.call(  # noqa: DUO116
                    (GCPHandler.MACHINE_STOPPING_COMMAND % (" ".join(machine_list[zone]), zone)),
                    shell=True,
                )
            LOGGER.info("GCP machines stopped successfully.")
        except Exception as e:
            LOGGER.error("GCP Handler failed to stop network machines: %s" % e)

    @staticmethod
    def get_auth_command(key_path):
        return GCPHandler.AUTHENTICATION_COMMAND % key_path

    @staticmethod
    def get_set_project_command(project):
        return GCPHandler.SET_PROPERTY_PROJECT % project
