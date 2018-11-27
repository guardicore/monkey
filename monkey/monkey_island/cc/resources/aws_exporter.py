import logging
import uuid
from datetime import datetime
import boto3

from cc.resources.exporter import Exporter
from cc.services.config import ConfigService
from cc.environment.environment import load_server_configuration_from_file

logger = logging.getLogger(__name__)

AWS_CRED_CONFIG_KEYS = [['cnc', 'aws_config', 'aws_access_key_id'],
                        ['cnc', 'aws_config', 'aws_secret_access_key'],
                        ['cnc', 'aws_config', 'aws_account_id']]


class AWSExporter(Exporter):

    @staticmethod
    def handle_report(report_json):

        findings_list = []
        issues_list = report_json['recommendations']['issues']
        if not issues_list:
            logger.info('No issues were found by the monkey, no need to send anything')
            return True
        for machine in issues_list:
            for issue in issues_list[machine]:
                findings_list.append(AWSExporter._prepare_finding(issue))

        if not AWSExporter._send_findings(findings_list, AWSExporter._get_aws_keys()):
            logger.error('Exporting findings to aws failed')
            return False

        return True

    @staticmethod
    def _get_aws_keys():
        creds_dict = {}
        for key in AWS_CRED_CONFIG_KEYS:
            creds_dict[key[2]] = str(ConfigService.get_config_value(key))

        return creds_dict

    @staticmethod
    def merge_two_dicts(x, y):
        z = x.copy()  # start with x's keys and values
        z.update(y)  # modifies z with y's keys and values & returns None
        return z

    @staticmethod
    def _prepare_finding(issue):
        findings_dict = {
            'island_cross_segment': AWSExporter._handle_island_cross_segment_issue,
            'ssh': AWSExporter._handle_ssh_issue,
            'shellshock': AWSExporter._handle_shellshock_issue,
            'tunnel': AWSExporter._handle_tunnel_issue,
            'elastic': AWSExporter._handle_elastic_issue,
            'smb_password': AWSExporter._handle_smb_password_issue,
            'smb_pth': AWSExporter._handle_smb_pth_issue,
            'sambacry': AWSExporter._handle_sambacry_issue,
            'shared_passwords': AWSExporter._handle_shared_passwords_issue,
            'wmi_password': AWSExporter._handle_wmi_password_issue,
            'wmi_pth': AWSExporter._handle_wmi_pth_issue,
            'ssh_key': AWSExporter._handle_ssh_key_issue,
            'rdp': AWSExporter._handle_rdp_issue,
            'shared_passwords_domain': AWSExporter._handle_shared_passwords_domain_issue,
            'shared_admins_domain': AWSExporter._handle_shared_admins_domain_issue,
            'strong_users_on_crit': AWSExporter._handle_strong_users_on_crit_issue,
            'struts2': AWSExporter._handle_struts2_issue,
            'weblogic': AWSExporter._handle_weblogic_issue,
            'hadoop': AWSExporter._handle_hadoop_issue,
            # azure and conficker are not relevant issues for an AWS env
        }

        product_arn = load_server_configuration_from_file()['aws'].get('sec_hub_product_arn', '')
        account_id = AWSExporter._get_aws_keys().get('aws_account_id', '')

        finding = {
            "SchemaVersion": "2018-10-08",
            "Id": uuid.uuid4().hex,
            "ProductArn": product_arn,
            "GeneratorId": issue['type'],
            "AwsAccountId": account_id,
            "Types": [
                "Software and Configuration Checks/Vulnerabilities/CVE"
            ],
            "CreatedAt": datetime.now().isoformat() + 'Z',
            "UpdatedAt": datetime.now().isoformat() + 'Z',
        }
        return AWSExporter.merge_two_dicts(finding, findings_dict[issue['type']](issue))

    @staticmethod
    def _send_findings(findings_list, creds_dict):

        securityhub = boto3.client('securityhub',
                                   aws_access_key_id=creds_dict.get('aws_access_key_id', ''),
                                   aws_secret_access_key=creds_dict.get('aws_secret_access_key', ''))
        try:
            import_response = securityhub.batch_import_findings(Findings=findings_list)
            print import_response
            if import_response['ResponseMetadata']['HTTPStatusCode'] == 200:
                return True
            else:
                return False
        except Exception as e:
            logger.error('AWS security hub findings failed to send.')
            return False

    @staticmethod
    def _handle_tunnel_issue(issue):
        finding = \
            {"Severity": {
                "Product": 5,
                "Normalized": 100
            }, "Resources": [{
                "Type": "AwsEc2Instance",
                "Id": issue['aws_instance_id']
            }], "RecordState": "ACTIVE",
                "Title": "Weak segmentation - Machines were able to communicate over unused ports.",
                "Description": "Use micro-segmentation policies to disable communication other than the required.",
                "Remediation": {
                    "Recommendation": {
                        "Text": "Machines are not locked down at port level. Network tunnel was set up from {0} to {1}"
                            .format(issue['machine'], issue['dest'])
                    }
                }}

        return finding

    @staticmethod
    def _handle_sambacry_issue(issue):
        finding = \
            {"Severity": {
                "Product": 10,
                "Normalized": 100
            }, "Resources": [{
                "Type": "AwsEc2Instance",
                "Id": issue['aws_instance_id']
            }], "RecordState": "ACTIVE", "Title": "Samba servers are vulnerable to 'SambaCry'",
                "Description": "Change {0} password to a complex one-use password that is not shared with other computers on the network. Update your Samba server to 4.4.14 and up, 4.5.10 and up, or 4.6.4 and up." \
                    .format(issue['username']), "Remediation": {
                "Recommendation": {
                    "Text": "The machine {0} ({1}) is vulnerable to a SambaCry attack. The Monkey authenticated over the SMB protocol with user {2} and its password, and used the SambaCry vulnerability.".format(
                        issue['machine'], issue['ip_address'], issue['username'])
                }
            }}

        return finding

    @staticmethod
    def _handle_smb_pth_issue(issue):
        finding = \
            {"Severity": {
                "Product": 5,
                "Normalized": 100
            }, "Resources": [{
                "Type": "AwsEc2Instance",
                "Id": issue['aws_instance_id']
            }], "RecordState": "ACTIVE",
                "Title": "Machines are accessible using passwords supplied by the user during the Monkey's configuration.",
                "Description": "Change {0}'s password to a complex one-use password that is not shared with other computers on the network.".format(
                    issue['username']), "Remediation": {
                "Recommendation": {
                    "Text": "The machine {0}({1}) is vulnerable to a SMB attack. The Monkey used a pass-the-hash attack over SMB protocol with user {2}.".format(
                        issue['machine'], issue['ip_address'], issue['username'])
                }
            }}

        return finding

    @staticmethod
    def _handle_ssh_issue(issue):
        finding = \
            {"Severity": {
                "Product": 1,
                "Normalized": 100
            }, "Resources": [{
                "Type": "AwsEc2Instance",
                "Id": issue['aws_instance_id']
            }], "RecordState": "ACTIVE",
                "Title": "Machines are accessible using SSH passwords supplied by the user during the Monkey's configuration.",
                "Description": "Change {0}'s password to a complex one-use password that is not shared with other computers on the network.".format(
                    issue['username']), "Remediation": {
                "Recommendation": {
                    "Text": "The machine {0} ({1}) is vulnerable to a SSH attack. The Monkey authenticated over the SSH protocol with user {2} and its password.".format(
                        issue['machine'], issue['ip_address'], issue['username'])
                }
            }}

        return finding

    @staticmethod
    def _handle_ssh_key_issue(issue):
        finding = \
            {"Severity": {
                "Product": 1,
                "Normalized": 100
            }, "Resources": [{
                "Type": "AwsEc2Instance",
                "Id": issue['aws_instance_id']
            }], "RecordState": "ACTIVE",
                "Title": "Machines are accessible using SSH passwords supplied by the user during the Monkey's configuration.",
                "Description": "Protect {ssh_key} private key with a pass phrase.".format(ssh_key=issue['ssh_key']),
                "Remediation": {
                    "Recommendation": {
                        "Text": "The machine {machine} ({ip_address}) is vulnerable to a SSH attack. The Monkey authenticated over the SSH protocol with private key {ssh_key}.".format(
                            machine=issue['machine'], ip_address=issue['ip_address'], ssh_key=issue['ssh_key'])
                    }
                }}

        return finding

    @staticmethod
    def _handle_elastic_issue(issue):
        finding = \
            {"Severity": {
                "Product": 10,
                "Normalized": 100
            }, "Resources": [{
                "Type": "AwsEc2Instance",
                "Id": issue['aws_instance_id']
            }], "RecordState": "ACTIVE", "Title": "Elasticsearch servers are vulnerable to CVE-2015-1427",
                "Description": "Update your Elastic Search server to version 1.4.3 and up.", "Remediation": {
                "Recommendation": {
                    "Text": "The machine {0}({1}) is vulnerable to an Elastic Groovy attack. The attack was made possible because the Elastic Search server was not patched against CVE-2015-1427.".format(
                        issue['machine'], issue['ip_address'])
                }
            }}

        return finding

    @staticmethod
    def _handle_island_cross_segment_issue(issue):
        finding = \
            {"Severity": {
                "Product": 1,
                "Normalized": 100
            }, "Resources": [{
                "Type": "AwsEc2Instance",
                "Id": issue['aws_instance_id']
            }], "RecordState": "ACTIVE",
                "Title": "Weak segmentation - Machines from different segments are able to communicate.",
                "Description": "Segment your network and make sure there is no communication between machines from different segments.",
                "Remediation": {
                    "Recommendation": {
                        "Text": "The network can probably be segmented. A monkey instance on \
                        {0} in the networks {1} \
                        could directly access the Monkey Island server in the networks {2}.".format(issue['machine'],
                                                                                                    issue['networks'],
                                                                                                    issue['server_networks'])
                    }
                }}

        return finding

    @staticmethod
    def _handle_shared_passwords_issue(issue):
        finding = \
            {"Severity": {
                "Product": 1,
                "Normalized": 100
            }, "Resources": [{
                "Type": "AwsEc2Instance",
                "Id": issue['aws_instance_id']
            }], "RecordState": "ACTIVE", "Title": "Multiple users have the same password",
                "Description": "Some users are sharing passwords, this should be fixed by changing passwords.",
                "Remediation": {
                    "Recommendation": {
                        "Text": "These users are sharing access password: {0}.".format(issue['shared_with'])
                    }
                }}

        return finding

    @staticmethod
    def _handle_shellshock_issue(issue):
        finding = \
            {"Severity": {
                "Product": 10,
                "Normalized": 100
            }, "Resources": [{
                "Type": "AwsEc2Instance",
                "Id": issue['aws_instance_id']
            }], "RecordState": "ACTIVE", "Title": "Machines are vulnerable to 'Shellshock'",
                "Description": "Update your Bash to a ShellShock-patched version.", "Remediation": {
                "Recommendation": {
                    "Text": "The machine {0} ({1}) is vulnerable to a ShellShock attack. "
                            "The attack was made possible because the HTTP server running on TCP port {2} was vulnerable to a shell injection attack on the paths: {3}.".format(
                        issue['machine'], issue['ip_address'], issue['port'], issue['paths'])
                }
            }}

        return finding

    @staticmethod
    def _handle_smb_password_issue(issue):
        finding = \
            {"Severity": {
                "Product": 1,
                "Normalized": 100
            }, "Resources": [{
                "Type": "AwsEc2Instance",
                "Id": issue['aws_instance_id']
            }], "RecordState": "ACTIVE",
                "Title": "Machines are accessible using passwords supplied by the user during the Monkey's configuration.",
                "Description": "Change {0}'s password to a complex one-use password that is not shared with other computers on the network.".format(
                    issue['username']), "Remediation": {
                "Recommendation": {
                    "Text": "The machine {0} ({1}) is vulnerable to a SMB attack. The Monkey authenticated over the SMB protocol with user {2} and its password.".format(
                        issue['machine'], issue['ip_address'], issue['username'])
                }
            }}

        return finding

    @staticmethod
    def _handle_wmi_password_issue(issue):
        finding = \
            {"Severity": {
                "Product": 1,
                "Normalized": 100
            }, "Resources": [{
                "Type": "AwsEc2Instance",
                "Id": issue['aws_instance_id']
            }], "RecordState": "ACTIVE",
                "Title": "Machines are accessible using passwords supplied by the user during the Monkey's configuration.",
                "Description": "Change {0}'s password to a complex one-use password that is not shared with other computers on the network.",
                "Remediation": {
                    "Recommendation": {
                        "Text": "The machine machine ({ip_address}) is vulnerable to a WMI attack. The Monkey authenticated over the WMI protocol with user {username} and its password.".format(
                            machine=issue['machine'], ip_address=issue['ip_address'], username=issue['username'])
                    }
                }}

        return finding

    @staticmethod
    def _handle_wmi_pth_issue(issue):
        finding = \
            {"Severity": {
                "Product": 1,
                "Normalized": 100
            }, "Resources": [{
                "Type": "AwsEc2Instance",
                "Id": issue['aws_instance_id']
            }], "RecordState": "ACTIVE",
                "Title": "Machines are accessible using passwords supplied by the user during the Monkey's configuration.",
                "Description": "Change {0}'s password to a complex one-use password that is not shared with other computers on the network.".format(
                    issue['username']), "Remediation": {
                "Recommendation": {
                    "Text": "The machine machine ({ip_address}) is vulnerable to a WMI attack. The Monkey used a pass-the-hash attack over WMI protocol with user {username}".format(
                        machine=issue['machine'], ip_address=issue['ip_address'], username=issue['username'])
                }
            }}

        return finding

    @staticmethod
    def _handle_rdp_issue(issue):
        finding = \
            {"Severity": {
                "Product": 1,
                "Normalized": 100
            }, "Resources": [{
                "Type": "AwsEc2Instance",
                "Id": issue['aws_instance_id']
            }], "RecordState": "ACTIVE",
                "Title": "Machines are accessible using passwords supplied by the user during the Monkey's configuration.",
                "Description": "Change {0}'s password to a complex one-use password that is not shared with other computers on the network.".format(
                    issue['username']), "Remediation": {
                "Recommendation": {
                    "Text": "The machine machine ({ip_address}) is vulnerable to a RDP attack. The Monkey authenticated over the RDP protocol with user {username} and its password.".format(
                        machine=issue['machine'], ip_address=issue['ip_address'], username=issue['username'])
                }
            }}

        return finding

    @staticmethod
    def _handle_shared_passwords_domain_issue(issue):
        finding = \
            {"Severity": {
                "Product": 1,
                "Normalized": 100
            }, "Resources": [{
                "Type": "AwsEc2Instance",
                "Id": issue['aws_instance_id']
            }], "RecordState": "ACTIVE", "Title": "Multiple users have the same password.",
                "Description": "Some domain users are sharing passwords, this should be fixed by changing passwords.",
                "Remediation": {
                    "Recommendation": {
                        "Text": "These users are sharing access password: {shared_with}.".format(
                            shared_with=issue['shared_with'])
                    }
                }}

        return finding

    @staticmethod
    def _handle_shared_admins_domain_issue(issue):
        finding = \
            {"Severity": {
                "Product": 1,
                "Normalized": 100
            }, "Resources": [{
                "Type": "AwsEc2Instance",
                "Id": issue['aws_instance_id']
            }], "RecordState": "ACTIVE",
                "Title": "Shared local administrator account - Different machines have the same account as a local administrator.",
                "Description": "Make sure the right administrator accounts are managing the right machines, and that there isn\'t an unintentional local admin sharing.",
                "Remediation": {
                    "Recommendation": {
                        "Text": "Here is a list of machines which the account {username} is defined as an administrator: {shared_machines}".format(
                            username=issue['username'], shared_machines=issue['shared_machines'])
                    }
                }}

        return finding

    @staticmethod
    def _handle_strong_users_on_crit_issue(issue):
        finding = \
            {"Severity": {
                "Product": 1,
                "Normalized": 100
            }, "Resources": [{
                "Type": "AwsEc2Instance",
                "Id": issue['aws_instance_id']
            }], "RecordState": "ACTIVE",
                "Title": "Mimikatz found login credentials of a user who has admin access to a server defined as critical.",
                "Description": "This critical machine is open to attacks via strong users with access to it.",
                "Remediation": {
                    "Recommendation": {
                        "Text": "The services: {services} have been found on the machine thus classifying it as a critical machine. These users has access to it:{threatening_users}.".format(
                            services=issue['services'], threatening_users=issue['threatening_users'])
                    }
                }}

        return finding

    @staticmethod
    def _handle_struts2_issue(issue):
        finding = \
            {"Severity": {
                "Product": 10,
                "Normalized": 100
            }, "Resources": [{
                "Type": "AwsEc2Instance",
                "Id": issue['aws_instance_id']
            }], "RecordState": "ACTIVE", "Title": "Struts2 servers are vulnerable to remote code execution.",
                "Description": "Upgrade Struts2 to version 2.3.32 or 2.5.10.1 or any later versions.", "Remediation": {
                "Recommendation": {
                    "Text": "Struts2 server at {machine} ({ip_address}) is vulnerable to remote code execution attack."
                            " The attack was made possible because the server is using an old version of Jakarta based file upload Multipart parser.".format(
                        machine=issue['machine'], ip_address=issue['ip_address'])
                }
            }}

        return finding

    @staticmethod
    def _handle_weblogic_issue(issue):
        finding = \
            {"Severity": {
                "Product": 10,
                "Normalized": 100
            }, "Resources": [{
                "Type": "AwsEc2Instance",
                "Id": issue['aws_instance_id']
            }], "RecordState": "ACTIVE", "Title": "Oracle WebLogic servers are vulnerable to remote code execution.",
                "Description": "Install Oracle critical patch updates. Or update to the latest version. " \
                               "Vulnerable versions are 10.3.6.0.0, 12.1.3.0.0, 12.2.1.1.0 and 12.2.1.2.0.",
                "Remediation": {
                    "Recommendation": {
                        "Text": "Oracle WebLogic server at {machine} ({ip_address}) is vulnerable to remote code execution attack."
                                " The attack was made possible due to incorrect permission assignment in Oracle Fusion Middleware (subcomponent: WLS Security).".format(
                            machine=issue['machine'], ip_address=issue['ip_address'])
                    }
                }}

        return finding

    @staticmethod
    def _handle_hadoop_issue(issue):
        finding = \
            {"Severity": {
                "Product": 10,
                "Normalized": 100
            }, "Resources": [{
                "Type": "AwsEc2Instance",
                "Id": issue['aws_instance_id']
            }], "RecordState": "ACTIVE", "Title": "Hadoop/Yarn servers are vulnerable to remote code execution.",
                "Description": "Run Hadoop in secure mode, add Kerberos authentication.", "Remediation": {
                "Recommendation": {
                    "Text": "The Hadoop server at {machine} ({ip_address}) is vulnerable to remote code execution attack."
                            " The attack was made possible due to default Hadoop/Yarn configuration being insecure."
                }
            }}

        return finding
