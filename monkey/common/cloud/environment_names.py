from enum import Enum


class Environment(Enum):
    UNKNOWN = "Unknown"
    ON_PREMISE = "On Premise"
    AZURE = "Azure"
    AWS = "AWS"
    GCP = "GCP"
    ALIBABA = "Alibaba Cloud"
    IBM = "IBM Cloud"
    DigitalOcean = "Digital Ocean"


ALL_ENVIRONMENTS_NAMES = [x.value for x in Environment]
