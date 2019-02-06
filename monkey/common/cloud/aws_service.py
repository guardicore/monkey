import boto3
from botocore.exceptions import ClientError

__author__ = 'itay.mizeretz'


class AwsService(object):
    """
    Supplies various AWS services
    """

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

    @staticmethod
    def test_client():
        try:
            AwsService.get_client('ssm').describe_instance_information()
            return True
        except ClientError:
            return False

    @staticmethod
    def get_instances():
        return \
            [
                {
                    'instance_id': x['InstanceId'],
                    'name': x['ComputerName'],
                    'os': x['PlatformType'].lower(),
                    'ip_address': x['IPAddress']
                }
                for x in AwsService.get_client('ssm').describe_instance_information()['InstanceInformationList']
            ]

