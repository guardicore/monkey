from connectors.vcenter import VCenterJob, VCenterConnector
from connectors.demo import DemoJob, DemoConnector

available_jobs = [VCenterJob, DemoJob]


def get_connector_by_name(name):
    for jobclass in available_jobs:
        if name == jobclass.connector.__name__:
            return jobclass.connector()
    return None


def get_jobclass_by_name(name):
    for jobclass in available_jobs:
        if jobclass.__name__ == name:
            return jobclass


def refresh_connector_config(mongo, connector):
    properties = mongo.db.connector.find_one({"type": connector.__class__.__name__})
    if properties:
        connector.load_properties(properties)


def load_connector(mongo, name):
    con = get_connector_by_name(name)
    if not con:
        return None
    refresh_connector_config(mongo, con)
    return con