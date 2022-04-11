import logging
import uuid
from datetime import datetime

import boto3
from botocore.exceptions import UnknownServiceError

from common.cloud.aws.aws_instance import AwsInstance
from monkey_island.cc.services.reporting.exporter import Exporter

__authors__ = ["maor.rayzin", "shay.nehmad"]


from monkey_island.cc.services.reporting.issue_processing.exploit_processing.exploiter_descriptor_enum import (  # noqa:E501 (Long import)
    ExploiterDescriptorEnum,
)

# noqa:E501 (Long import)
from monkey_island.cc.services.reporting.issue_processing.exploit_processing.exploiter_report_info import (  # noqa:E501 (Long import)
    CredentialType,
)

logger = logging.getLogger(__name__)

INFECTION_MONKEY_ARN = "324264561773:product/guardicore/aws-infection-monkey"


class AWSExporter(Exporter):
    @staticmethod
    def handle_report(report_json):

        findings_list = []
        issues_list = report_json["recommendations"]["issues"]
        if not issues_list:
            logger.info("No issues were found by the monkey, no need to send anything")
            return True

        # Not suppressing error here on purpose.
        current_aws_region = AwsInstance().get_region()

        for machine in issues_list:
            for issue in issues_list[machine]:
                try:
                    if "aws_instance_id" in issue:
                        findings_list.append(
                            AWSExporter._prepare_finding(issue, current_aws_region)
                        )
                except AWSExporter.FindingNotFoundError as e:
                    logger.error(e)

        if not AWSExporter._send_findings(findings_list, current_aws_region):
            logger.error("Exporting findings to aws failed")
            return False

        return True

    @staticmethod
    def merge_two_dicts(x, y):
        z = x.copy()  # start with x's keys and values
        z.update(y)  # modifies z with y's keys and values & returns None
        return z

    @staticmethod
    def _prepare_finding(issue, region):
        findings_dict = {
            "island_cross_segment": AWSExporter._handle_island_cross_segment_issue,
            ExploiterDescriptorEnum.SSH.value.class_name: {
                CredentialType.PASSWORD.value: AWSExporter._handle_ssh_issue,
                CredentialType.KEY.value: AWSExporter._handle_ssh_key_issue,
            },
            "tunnel": AWSExporter._handle_tunnel_issue,
            ExploiterDescriptorEnum.SMB.value.class_name: {
                CredentialType.PASSWORD.value: AWSExporter._handle_smb_password_issue,
                CredentialType.HASH.value: AWSExporter._handle_smb_pth_issue,
            },
            "shared_passwords": AWSExporter._handle_shared_passwords_issue,
            ExploiterDescriptorEnum.WMI.value.class_name: {
                CredentialType.PASSWORD.value: AWSExporter._handle_wmi_password_issue,
                CredentialType.HASH.value: AWSExporter._handle_wmi_pth_issue,
            },
            "shared_passwords_domain": AWSExporter._handle_shared_passwords_domain_issue,
            "shared_admins_domain": AWSExporter._handle_shared_admins_domain_issue,
            "strong_users_on_crit": AWSExporter._handle_strong_users_on_crit_issue,
            ExploiterDescriptorEnum.HADOOP.value.class_name: AWSExporter._handle_hadoop_issue,
        }

        configured_product_arn = INFECTION_MONKEY_ARN
        product_arn = "arn:aws:securityhub:{region}:{arn}".format(
            region=region, arn=configured_product_arn
        )
        instance_arn = "arn:aws:ec2:" + str(region) + ":instance:{instance_id}"
        # Not suppressing error here on purpose.
        account_id = AwsInstance().get_account_id()
        logger.debug("aws account id acquired: {}".format(account_id))

        aws_finding = {
            "SchemaVersion": "2018-10-08",
            "Id": uuid.uuid4().hex,
            "ProductArn": product_arn,
            "GeneratorId": issue["type"],
            "AwsAccountId": account_id,
            "RecordState": "ACTIVE",
            "Types": ["Software and Configuration Checks/Vulnerabilities/CVE"],
            "CreatedAt": datetime.now().isoformat() + "Z",
            "UpdatedAt": datetime.now().isoformat() + "Z",
        }

        processor = AWSExporter._get_issue_processor(findings_dict, issue)

        return AWSExporter.merge_two_dicts(aws_finding, processor(issue, instance_arn))

    @staticmethod
    def _get_issue_processor(finding_dict, issue):
        try:
            processor = finding_dict[issue["type"]]
            if type(processor) == dict:
                processor = processor[issue["credential_type"]]
            return processor
        except KeyError:
            raise AWSExporter.FindingNotFoundError(
                f"Finding {issue['type']} not added as AWS exportable finding"
            )

    class FindingNotFoundError(Exception):
        pass

    @staticmethod
    def _send_findings(findings_list, region):
        try:
            logger.debug("Trying to acquire securityhub boto3 client in " + region)
            security_hub_client = boto3.client("securityhub", region_name=region)
            logger.debug("Client acquired: {0}".format(repr(security_hub_client)))

            # Assumes the machine has the correct IAM role to do this, @see
            # https://github.com/guardicore/monkey/wiki/Monkey-Island:-Running-the-monkey-on-AWS
            # -EC2-instances
            import_response = security_hub_client.batch_import_findings(Findings=findings_list)
            logger.debug("Import findings response: {0}".format(repr(import_response)))

            if import_response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                return True
            else:
                return False
        except UnknownServiceError as e:
            logger.warning(
                "AWS exporter called but AWS-CLI security hub service is not installed. "
                "Error: {}".format(e)
            )
            return False
        except Exception as e:
            logger.exception("AWS security hub findings failed to send. Error: {}".format(e))
            return False

    @staticmethod
    def _get_finding_resource(instance_id, instance_arn):
        if instance_id:
            return [{"Type": "AwsEc2Instance", "Id": instance_arn.format(instance_id=instance_id)}]
        else:
            return [{"Type": "Other", "Id": "None"}]

    @staticmethod
    def _build_generic_finding(
        severity, title, description, recommendation, instance_arn, instance_id=None
    ):
        finding = {
            "Severity": {"Product": severity, "Normalized": 100},
            "Resources": AWSExporter._get_finding_resource(instance_id, instance_arn),
            "Title": title,
            "Description": description,
            "Remediation": {"Recommendation": {"Text": recommendation}},
        }

        return finding

    @staticmethod
    def _handle_tunnel_issue(issue, instance_arn):

        return AWSExporter._build_generic_finding(
            severity=5,
            title="Weak segmentation - Machines were able to communicate over unused ports.",
            description="Use micro-segmentation policies to disable communication other than "
            "the required.",
            recommendation="Machines are not locked down at port level. "
            "Network tunnel was set up from {0} to {1}".format(issue["machine"], issue["dest"]),
            instance_arn=instance_arn,
            instance_id=issue["aws_instance_id"] if "aws_instance_id" in issue else None,
        )

    @staticmethod
    def _handle_smb_pth_issue(issue, instance_arn):

        return AWSExporter._build_generic_finding(
            severity=5,
            title="Machines are accessible using passwords supplied by the user during the "
            "Monkey's configuration.",
            description="Change {0}'s password to a complex one-use password that is not "
            "shared with other computers on the "
            "network.".format(issue["username"]),
            recommendation="The machine {0}({1}) is vulnerable to a SMB attack. The Monkey "
            "used a pass-the-hash attack over "
            "SMB protocol with user {2}.".format(
                issue["machine"], issue["ip_address"], issue["username"]
            ),
            instance_arn=instance_arn,
            instance_id=issue["aws_instance_id"] if "aws_instance_id" in issue else None,
        )

    @staticmethod
    def _handle_ssh_issue(issue, instance_arn):

        return AWSExporter._build_generic_finding(
            severity=1,
            title="Machines are accessible using SSH passwords supplied by the user during "
            "the Monkey's configuration.",
            description="Change {0}'s password to a complex one-use password that is not "
            "shared with other computers on the "
            "network.".format(issue["username"]),
            recommendation="The machine {0} ({1}) is vulnerable to a SSH attack. The Monkey "
            "authenticated over the SSH"
            " protocol with user {2} and its "
            "password.".format(issue["machine"], issue["ip_address"], issue["username"]),
            instance_arn=instance_arn,
            instance_id=issue["aws_instance_id"] if "aws_instance_id" in issue else None,
        )

    @staticmethod
    def _handle_ssh_key_issue(issue, instance_arn):

        return AWSExporter._build_generic_finding(
            severity=1,
            title="Machines are accessible using SSH passwords supplied by the user during "
            "the Monkey's configuration.",
            description="Protect {ssh_key} private key with a pass phrase.".format(
                ssh_key=issue["ssh_key"]
            ),
            recommendation="The machine {machine} ({ip_address}) is vulnerable to a SSH "
            "attack. The Monkey authenticated "
            "over the SSH protocol with private key {ssh_key}.".format(
                machine=issue["machine"], ip_address=issue["ip_address"], ssh_key=issue["ssh_key"]
            ),
            instance_arn=instance_arn,
            instance_id=issue["aws_instance_id"] if "aws_instance_id" in issue else None,
        )

    @staticmethod
    def _handle_island_cross_segment_issue(issue, instance_arn):

        return AWSExporter._build_generic_finding(
            severity=1,
            title="Weak segmentation - Machines from different segments are able to "
            "communicate.",
            description="Segment your network and make sure there is no communication between "
            "machines from different "
            "segments.",
            recommendation="The network can probably be segmented. A monkey instance on \
                        {0} in the networks {1} \
                        could directly access the Monkey Island server in the networks {2}.".format(
                issue["machine"], issue["networks"], issue["server_networks"]
            ),
            instance_arn=instance_arn,
            instance_id=issue["aws_instance_id"] if "aws_instance_id" in issue else None,
        )

    @staticmethod
    def _handle_shared_passwords_issue(issue, instance_arn):

        return AWSExporter._build_generic_finding(
            severity=1,
            title="Multiple users have the same password",
            description="Some users are sharing passwords, this should be fixed by changing "
            "passwords.",
            recommendation="These users are sharing access password: {0}.".format(
                issue["shared_with"]
            ),
            instance_arn=instance_arn,
            instance_id=issue["aws_instance_id"] if "aws_instance_id" in issue else None,
        )

    @staticmethod
    def _handle_smb_password_issue(issue, instance_arn):

        return AWSExporter._build_generic_finding(
            severity=1,
            title="Machines are accessible using passwords supplied by the user during the "
            "Monkey's configuration.",
            description="Change {0}'s password to a complex one-use password that is not "
            "shared with other computers on the "
            "network.".format(issue["username"]),
            recommendation="The machine {0} ({1}) is vulnerable to a SMB attack. The Monkey "
            "authenticated over the SMB "
            "protocol with user {2} and its password.".format(
                issue["machine"], issue["ip_address"], issue["username"]
            ),
            instance_arn=instance_arn,
            instance_id=issue["aws_instance_id"] if "aws_instance_id" in issue else None,
        )

    @staticmethod
    def _handle_wmi_password_issue(issue, instance_arn):

        return AWSExporter._build_generic_finding(
            severity=1,
            title="Machines are accessible using passwords supplied by the user during the "
            "Monkey's configuration.",
            description="Change {0}'s password to a complex one-use password that is not "
            "shared with other computers on the "
            "network.",
            recommendation="The machine {machine} ({ip_address}) is vulnerable to a WMI "
            "attack. The Monkey authenticated over "
            "the WMI protocol with user {username} and its password.".format(
                machine=issue["machine"], ip_address=issue["ip_address"], username=issue["username"]
            ),
            instance_arn=instance_arn,
            instance_id=issue["aws_instance_id"] if "aws_instance_id" in issue else None,
        )

    @staticmethod
    def _handle_wmi_pth_issue(issue, instance_arn):

        return AWSExporter._build_generic_finding(
            severity=1,
            title="Machines are accessible using passwords supplied by the user during the "
            "Monkey's configuration.",
            description="Change {0}'s password to a complex one-use password that is not "
            "shared with other computers on the "
            "network.".format(issue["username"]),
            recommendation="The machine {machine} ({ip_address}) is vulnerable to a WMI "
            "attack. The Monkey used a "
            "pass-the-hash attack over WMI protocol with user {username}".format(
                machine=issue["machine"], ip_address=issue["ip_address"], username=issue["username"]
            ),
            instance_arn=instance_arn,
            instance_id=issue["aws_instance_id"] if "aws_instance_id" in issue else None,
        )

    @staticmethod
    def _handle_shared_passwords_domain_issue(issue, instance_arn):

        return AWSExporter._build_generic_finding(
            severity=1,
            title="Multiple users have the same password.",
            description="Some domain users are sharing passwords, this should be fixed by "
            "changing passwords.",
            recommendation="These users are sharing access password: {shared_with}.".format(
                shared_with=issue["shared_with"]
            ),
            instance_arn=instance_arn,
            instance_id=issue["aws_instance_id"] if "aws_instance_id" in issue else None,
        )

    @staticmethod
    def _handle_shared_admins_domain_issue(issue, instance_arn):

        return AWSExporter._build_generic_finding(
            severity=1,
            title="Shared local administrator account - Different machines have the same "
            "account as a local administrator.",
            description="Make sure the right administrator accounts are managing the right "
            "machines, and that there isn't "
            "an unintentional local admin sharing.",
            recommendation="Here is a list of machines which the account {username} is "
            "defined as an administrator: "
            "{shared_machines}".format(
                username=issue["username"], shared_machines=issue["shared_machines"]
            ),
            instance_arn=instance_arn,
            instance_id=issue["aws_instance_id"] if "aws_instance_id" in issue else None,
        )

    @staticmethod
    def _handle_strong_users_on_crit_issue(issue, instance_arn):

        return AWSExporter._build_generic_finding(
            severity=1,
            title="Mimikatz found login credentials of a user who has admin access to a "
            "server defined as critical.",
            description="This critical machine is open to attacks via strong users with "
            "access to it.",
            recommendation="The services: {services} have been found on the machine thus "
            "classifying it as a critical "
            "machine. These users has access to it:{threatening_users}.".format(
                services=issue["services"], threatening_users=issue["threatening_users"]
            ),
            instance_arn=instance_arn,
            instance_id=issue["aws_instance_id"] if "aws_instance_id" in issue else None,
        )

    @staticmethod
    def _handle_hadoop_issue(issue, instance_arn):

        return AWSExporter._build_generic_finding(
            severity=10,
            title="Hadoop/Yarn servers are vulnerable to remote code execution.",
            description="Run Hadoop in secure mode, add Kerberos authentication.",
            recommendation="The Hadoop server at {machine} ({ip_address}) is vulnerable to "
            "remote code execution attack."
            "The attack was made possible due to default Hadoop/Yarn "
            "configuration being insecure.",
            instance_arn=instance_arn,
            instance_id=issue["aws_instance_id"] if "aws_instance_id" in issue else None,
        )
