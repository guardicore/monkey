import pytest
import requests
import requests_mock
import simplejson

from common.cloud.azure.azure_instance import (AZURE_METADATA_SERVICE_URL,
                                               AzureInstance)
from common.cloud.environment_names import Environment


GOOD_DATA = {
    'compute': {'azEnvironment': 'AZUREPUBLICCLOUD',
                'isHostCompatibilityLayerVm': 'true',
                'licenseType': 'Windows_Client',
                'location': 'westus',
                'name': 'examplevmname',
                'offer': 'Windows',
                'osProfile': {'adminUsername': 'admin',
                              'computerName': 'examplevmname',
                              'disablePasswordAuthentication': 'true'},
                'osType': 'linux',
                'placementGroupId': 'f67c14ab-e92c-408c-ae2d-da15866ec79a',
                'plan': {'name': 'planName',
                         'product': 'planProduct',
                         'publisher': 'planPublisher'},
                'platformFaultDomain': '36',
                'platformUpdateDomain': '42',
                'publicKeys': [{'keyData': 'ssh-rsa 0',
                                'path': '/home/user/.ssh/authorized_keys0'},
                               {'keyData': 'ssh-rsa 1',
                                'path': '/home/user/.ssh/authorized_keys1'}],
                'publisher': 'RDFE-Test-Microsoft-Windows-Server-Group',
                'resourceGroupName': 'macikgo-test-may-23',
                'resourceId': '/subscriptions/xxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx/resourceGroups/macikgo-test-may-23/'
                              'providers/Microsoft.Compute/virtualMachines/examplevmname',
                'securityProfile': {'secureBootEnabled': 'true',
                                    'virtualTpmEnabled': 'false'},
                'sku': 'Windows-Server-2012-R2-Datacenter',
                'storageProfile': {'dataDisks': [{'caching': 'None',
                                                  'createOption': 'Empty',
                                                  'diskSizeGB': '1024',
                                                  'image': {'uri': ''},
                                                  'lun': '0',
                                                  'managedDisk': {'id': '/subscriptions/xxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx/'
                                                                        'resourceGroups/macikgo-test-may-23/providers/'
                                                                        'Microsoft.Compute/disks/exampledatadiskname',
                                                                  'storageAccountType': 'Standard_LRS'},
                                                  'name': 'exampledatadiskname',
                                                  'vhd': {'uri': ''},
                                                  'writeAcceleratorEnabled': 'false'}],
                                   'imageReference': {'id': '',
                                                      'offer': 'UbuntuServer',
                                                      'publisher': 'Canonical',
                                                      'sku': '16.04.0-LTS',
                                                      'version': 'latest'},
                                   'osDisk': {'caching': 'ReadWrite',
                                              'createOption': 'FromImage',
                                              'diskSizeGB': '30',
                                              'diffDiskSettings': {'option': 'Local'},
                                              'encryptionSettings': {'enabled': 'false'},
                                              'image': {'uri': ''},
                                              'managedDisk': {'id': '/subscriptions/xxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx/'
                                                              'resourceGroups/macikgo-test-may-23/providers/'
                                                              'Microsoft.Compute/disks/exampleosdiskname',
                                                              'storageAccountType': 'Standard_LRS'},
                                              'name': 'exampleosdiskname',
                                              'osType': 'Linux',
                                              'vhd': {'uri': ''},
                                              'writeAcceleratorEnabled': 'false'}},
                'subscriptionId': 'xxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx',
                'tags': 'baz:bash;foo:bar',
                'version': '15.05.22',
                'vmId': '02aab8a4-74ef-476e-8182-f6d2ba4166a6',
                'vmScaleSetName': 'crpteste9vflji9',
                'vmSize': 'Standard_A3',
                'zone': ''},
    'network': {'interface': [{'ipv4': {'ipAddress': [{'privateIpAddress': '10.144.133.132',
                                                       'publicIpAddress': ''}],
                                        'subnet': [{'address': '10.144.133.128',
                                                    'prefix': '26'}]},
                               'ipv6': {'ipAddress': []},
                               'macAddress': '0011AAFFBB22'}]}
 }


BAD_DATA_NOT_JSON = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/\
xhtml1-transitional.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml">\n<head>\n<meta content="text/html; charset=utf-8" \
http-equiv="Content-Type" />\n<meta content="no-cache" http-equiv="Pragma" />\n<title>Waiting...</title>\n<script type="text/\
javascript">\nvar pageName = \'/\';\ntop.location.replace(pageName);\n</script>\n</head>\n<body> </body>\n</html>\n'


BAD_DATA_JSON = {'': ''}


def get_test_azure_instance(url, **kwargs):
    with requests_mock.Mocker() as m:
        m.get(url, **kwargs)
        test_azure_instance_object = AzureInstance()
        return test_azure_instance_object


# good request, good data
@pytest.fixture
def good_data_mock_instance():
    return get_test_azure_instance(AZURE_METADATA_SERVICE_URL, text=simplejson.dumps(GOOD_DATA))


def test_is_instance_good_data(good_data_mock_instance):
    assert good_data_mock_instance.is_instance()


def test_get_cloud_provider_name_good_data(good_data_mock_instance):
    assert good_data_mock_instance.get_cloud_provider_name() == Environment.AZURE


def test_try_parse_response_good_data(good_data_mock_instance):
    assert good_data_mock_instance.instance_name == GOOD_DATA['compute']['name']
    assert good_data_mock_instance.instance_id == GOOD_DATA['compute']['vmId']
    assert good_data_mock_instance.location == GOOD_DATA['compute']['location']


# good request, bad data (json)
@pytest.fixture
def bad_data_json_mock_instance():
    return get_test_azure_instance(AZURE_METADATA_SERVICE_URL, text=simplejson.dumps(BAD_DATA_JSON))


def test_is_instance_bad_data_json(bad_data_json_mock_instance):
    assert bad_data_json_mock_instance.is_instance() is False


def test_get_cloud_provider_name_bad_data_json(bad_data_json_mock_instance):
    assert bad_data_json_mock_instance.get_cloud_provider_name() == Environment.AZURE


def test_instance_attributes_bad_data_json(bad_data_json_mock_instance):
    assert bad_data_json_mock_instance.instance_name is None
    assert bad_data_json_mock_instance.instance_id is None
    assert bad_data_json_mock_instance.location is None


# good request, bad data (not json)
@pytest.fixture
def bad_data_not_json_mock_instance():
    return get_test_azure_instance(AZURE_METADATA_SERVICE_URL, text=BAD_DATA_NOT_JSON)


def test_is_instance_bad_data_not_json(bad_data_not_json_mock_instance):
    assert bad_data_not_json_mock_instance.is_instance() is False


def test_get_cloud_provider_name_bad_data_not_json(bad_data_not_json_mock_instance):
    assert bad_data_not_json_mock_instance.get_cloud_provider_name() == Environment.AZURE


def test_instance_attributes_bad_data_not_json(bad_data_not_json_mock_instance):
    assert bad_data_not_json_mock_instance.instance_name is None
    assert bad_data_not_json_mock_instance.instance_id is None
    assert bad_data_not_json_mock_instance.location is None


# bad request
@pytest.fixture
def bad_request_mock_instance():
    return get_test_azure_instance(AZURE_METADATA_SERVICE_URL, exc=requests.RequestException)


def test_is_instance_bad_request(bad_request_mock_instance):
    assert bad_request_mock_instance.is_instance() is False


def test_get_cloud_provider_name_bad_request(bad_request_mock_instance):
    assert bad_request_mock_instance.get_cloud_provider_name() == Environment.AZURE


def test_instance_attributes_bad_request(bad_request_mock_instance):
    assert bad_request_mock_instance.instance_name is None
    assert bad_request_mock_instance.instance_id is None
    assert bad_request_mock_instance.location is None


# not found request
@pytest.fixture
def not_found_request_mock_instance():
    return get_test_azure_instance(AZURE_METADATA_SERVICE_URL, status_code=404)


def test_is_instance_not_found_request(not_found_request_mock_instance):
    assert not_found_request_mock_instance.is_instance() is False


def test_get_cloud_provider_name_not_found_request(not_found_request_mock_instance):
    assert not_found_request_mock_instance.get_cloud_provider_name() == Environment.AZURE


def test_instance_attributes_not_found_request(not_found_request_mock_instance):
    assert not_found_request_mock_instance.instance_name is None
    assert not_found_request_mock_instance.instance_id is None
    assert not_found_request_mock_instance.location is None
