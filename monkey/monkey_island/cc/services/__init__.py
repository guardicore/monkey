from .authentication.authentication_service import AuthenticationService
from .authentication.json_file_user_datastore import JsonFileUserDatastore

from .aws import AWSService

# TODO: This is a temporary import to keep some tests passing. Remove it before merging #1928 to
#       develop.
from .aws import aws_service
