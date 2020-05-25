import logging
import subprocess

LOGGER = logging.getLogger(__name__)


class GCPHandler(object):

    AUTHENTICATION_COMMAND = "gcloud auth activate-service-account --key-file=%s"
    SET_PROPERTY_PROJECT = "gcloud config set project %s"
    MACHINE_STARTING_COMMAND = "gcloud compute instances start %s --zone=%s"
    MACHINE_STOPPING_COMMAND = "gcloud compute instances stop %s --zone=%s"

    def __init__(self, key_path="../gcp_keys/gcp_key.json", zone="europe-west3-a", project_id="guardicore-22050661"):
        self.zone = zone
        try:
            # pass the key file to gcp
            subprocess.call(GCPHandler.get_auth_command(key_path), shell=True)  # noqa: DUO116
            LOGGER.info("GCP Handler passed key")
            # set project
            subprocess.call(GCPHandler.get_set_project_command(project_id), shell=True)  # noqa: DUO116
            LOGGER.info("GCP Handler set project")
            LOGGER.info("GCP Handler initialized successfully")
        except Exception as e:
            LOGGER.error("GCP Handler failed to initialize: %s." % e)

    def start_machines(self, machine_list):
        """
        Start all the machines in the list.
        :param machine_list: A space-separated string with all the machine names. Example:
        start_machines(`" ".join(["elastic-3", "mssql-16"])`)
        """
        LOGGER.info("Setting up all GCP machines...")
        try:
            subprocess.call((GCPHandler.MACHINE_STARTING_COMMAND % (machine_list, self.zone)), shell=True)  # noqa: DUO116
            LOGGER.info("GCP machines successfully started.")
        except Exception as e:
            LOGGER.error("GCP Handler failed to start GCP machines: %s" % e)

    def stop_machines(self, machine_list):
        try:
            subprocess.call((GCPHandler.MACHINE_STOPPING_COMMAND % (machine_list, self.zone)), shell=True)  # noqa: DUO116
            LOGGER.info("GCP machines stopped successfully.")
        except Exception as e:
            LOGGER.error("GCP Handler failed to stop network machines: %s" % e)

    @staticmethod
    def get_auth_command(key_path):
        return GCPHandler.AUTHENTICATION_COMMAND % key_path

    @staticmethod
    def get_set_project_command(project):
        return GCPHandler.SET_PROPERTY_PROJECT % project
