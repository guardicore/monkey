import boto3

__author__ = 'itay.mizeretz'


class AwsService(object):
    """
    Supplies various AWS services
    """

    # TODO: consider changing from static to singleton, and generally change design
    access_key_id = None
    secret_access_key = None
    region = None

    @staticmethod
    def set_auth_params(access_key_id, secret_access_key):
        AwsService.access_key_id = access_key_id
        AwsService.secret_access_key = secret_access_key

    @staticmethod
    def set_region(region):
        AwsService.region = region

    @staticmethod
    def get_client(client_type, region=None):
        return boto3.client(
            client_type,
            aws_access_key_id=AwsService.access_key_id,
            aws_secret_access_key=AwsService.secret_access_key,
            region_name=region if region is not None else AwsService.region)

    @staticmethod
    def get_session():
        return boto3.session.Session(
            aws_access_key_id=AwsService.access_key_id,
            aws_secret_access_key=AwsService.secret_access_key)

    @staticmethod
    def get_regions():
        return AwsService.get_session().get_available_regions('ssm')
