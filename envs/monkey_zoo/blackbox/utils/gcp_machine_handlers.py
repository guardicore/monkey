import subprocess


class GCPHandler(object):

    AUTHENTICATION_COMMAND = "gcloud auth activate-service-account --key-file=%s"
    SET_PROPERTY_PROJECT = "gcloud config set project %s"
    MACHINE_STARTING_COMMAND = "gcloud compute instances start %s --zone=%s"
    MACHINE_STOPPING_COMMAND = "gcloud compute instances stop %s --zone=%s"

    def __init__(self, key_path="../gcp_keys/gcp_key.json", zone="europe-west3-a", project_id="guardicore-22050661"):
        self.zone = zone
        try:
            # pass the key file to gcp
            subprocess.call(GCPHandler.get_auth_command(key_path), shell=True)
            print("GCP Handler passed key")
            # set project
            subprocess.call(GCPHandler.get_set_project_command(project_id), shell=True)
            print("GCP Handler set project")
            print("GCP Handler initialized successfully")
        except Exception as e:
            print("GCP Handler failed to initialize: %s." % e)

    def start_machines(self, machine_list):
        print("Setting up all GCP machines...")
        try:
            subprocess.call((GCPHandler.MACHINE_STARTING_COMMAND % (machine_list, self.zone)), shell=True)
            print("GCP machines successfully started.")
        except Exception as e:
            print("GCP Handler failed to start GCP machines: %s" % e)

    def stop_machines(self, machine_list):
        try:
            subprocess.call((GCPHandler.MACHINE_STOPPING_COMMAND % (machine_list, self.zone)), shell=True)
            print("GCP machines stopped successfully.")
        except Exception as e:
            print("GCP Handler failed to stop network machines: %s" % e)

    @staticmethod
    def get_auth_command(key_path):
        return GCPHandler.AUTHENTICATION_COMMAND % key_path

    @staticmethod
    def get_set_project_command(project):
        return GCPHandler.SET_PROPERTY_PROJECT % project
