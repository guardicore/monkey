from abc import ABC, abstractmethod
from typing import List

from common.common_consts import zero_trust_consts
from monkey_island.cc.services.zero_trust.scoutsuite.consts.rule_names.cloudformation_rules import CloudformationRules
from monkey_island.cc.services.zero_trust.scoutsuite.consts.rule_names.cloudtrail_rules import CloudTrailRules
from monkey_island.cc.services.zero_trust.scoutsuite.consts.rule_names.cloudwatch_rules import CloudWatchRules
from monkey_island.cc.services.zero_trust.scoutsuite.consts.rule_names.config_rules import ConfigRules
from monkey_island.cc.services.zero_trust.scoutsuite.consts.rule_names.ec2_rules import EC2Rules
from monkey_island.cc.services.zero_trust.scoutsuite.consts.rule_names.elb_rules import ELBRules
from monkey_island.cc.services.zero_trust.scoutsuite.consts.rule_names.elbv2_rules import ELBv2Rules
from monkey_island.cc.services.zero_trust.scoutsuite.consts.rule_names.iam_rules import IAMRules
from monkey_island.cc.services.zero_trust.scoutsuite.consts.rule_names.rds_rules import RDSRules
from monkey_island.cc.services.zero_trust.scoutsuite.consts.rule_names.redshift_rules import RedshiftRules
from monkey_island.cc.services.zero_trust.scoutsuite.consts.rule_names.s3_rules import S3Rules
from monkey_island.cc.services.zero_trust.scoutsuite.consts.rule_names.ses_rules import SESRules
from monkey_island.cc.services.zero_trust.scoutsuite.consts.rule_names.sns_rules import SNSRules
from monkey_island.cc.services.zero_trust.scoutsuite.consts.rule_names.sqs_rules import SQSRules
from monkey_island.cc.services.zero_trust.scoutsuite.consts.rule_names.vpc_rules import VPCRules


# Class which links ZT tests and rules to ScoutSuite finding
class ScoutSuiteFindingMap(ABC):
    @property
    @abstractmethod
    def rules(self) -> List[EC2Rules]:
        pass

    @property
    @abstractmethod
    def test(self) -> str:
        pass


class PermissiveFirewallRules(ScoutSuiteFindingMap):
    rules = [EC2Rules.SECURITY_GROUP_ALL_PORTS_TO_ALL, EC2Rules.SECURITY_GROUP_OPENS_TCP_PORT_TO_ALL,
             EC2Rules.SECURITY_GROUP_OPENS_UDP_PORT_TO_ALL, EC2Rules.SECURITY_GROUP_OPENS_RDP_PORT_TO_ALL,
             EC2Rules.SECURITY_GROUP_OPENS_SSH_PORT_TO_ALL, EC2Rules.SECURITY_GROUP_OPENS_MYSQL_PORT_TO_ALL,
             EC2Rules.SECURITY_GROUP_OPENS_MSSQL_PORT_TO_ALL, EC2Rules.SECURITY_GROUP_OPENS_MONGODB_PORT_TO_ALL,
             EC2Rules.SECURITY_GROUP_OPENS_ORACLE_DB_PORT_TO_ALL, EC2Rules.SECURITY_GROUP_OPENS_POSTGRESQL_PORT_TO_ALL,
             EC2Rules.SECURITY_GROUP_OPENS_NFS_PORT_TO_ALL, EC2Rules.SECURITY_GROUP_OPENS_SMTP_PORT_TO_ALL,
             EC2Rules.SECURITY_GROUP_OPENS_DNS_PORT_TO_ALL, EC2Rules.SECURITY_GROUP_OPENS_ALL_PORTS_TO_SELF,
             EC2Rules.SECURITY_GROUP_OPENS_ALL_PORTS, EC2Rules.SECURITY_GROUP_OPENS_PLAINTEXT_PORT_FTP,
             EC2Rules.SECURITY_GROUP_OPENS_PLAINTEXT_PORT_TELNET, EC2Rules.SECURITY_GROUP_OPENS_PORT_RANGE,
             EC2Rules.EC2_SECURITY_GROUP_WHITELISTS_AWS,
             VPCRules.SUBNET_WITH_ALLOW_ALL_INGRESS_ACLS,
             VPCRules.SUBNET_WITH_ALLOW_ALL_EGRESS_ACLS,
             VPCRules.NETWORK_ACL_NOT_USED,
             VPCRules.DEFAULT_NETWORK_ACLS_ALLOW_ALL_INGRESS,
             VPCRules.DEFAULT_NETWORK_ACLS_ALLOW_ALL_EGRESS,
             VPCRules.CUSTOM_NETWORK_ACLS_ALLOW_ALL_INGRESS,
             VPCRules.CUSTOM_NETWORK_ACLS_ALLOW_ALL_EGRESS,
             RDSRules.RDS_SECURITY_GROUP_ALLOWS_ALL,
             RedshiftRules.REDSHIFT_SECURITY_GROUP_WHITELISTS_ALL
             ]

    test = zero_trust_consts.TEST_SCOUTSUITE_PERMISSIVE_FIREWALL_RULES


class UnencryptedData(ScoutSuiteFindingMap):
    rules = [EC2Rules.EBS_SNAPSHOT_NOT_ENCRYPTED, EC2Rules.EBS_VOLUME_NOT_ENCRYPTED,
             EC2Rules.EC2_INSTANCE_WITH_USER_DATA_SECRETS,
             ELBv2Rules.ELBV2_LISTENER_ALLOWING_CLEARTEXT, ELBv2Rules.ELBV2_OLDER_SSL_POLICY,
             RDSRules.RDS_INSTANCE_STORAGE_NOT_ENCRYPTED, RedshiftRules.REDSHIFT_CLUSTER_DATABASE_NOT_ENCRYPTED,
             RedshiftRules.REDSHIFT_PARAMETER_GROUP_SSL_NOT_REQUIRED,
             S3Rules.S3_BUCKET_ALLOWING_CLEARTEXT, S3Rules.S3_BUCKET_NO_DEFAULT_ENCRYPTION,
             ELBRules.ELB_LISTENER_ALLOWING_CLEARTEXT,
             ELBRules.ELB_OLDER_SSL_POLICY]

    test = zero_trust_consts.TEST_SCOUTSUITE_UNENCRYPTED_DATA


class DataLossPrevention(ScoutSuiteFindingMap):
    rules = [RDSRules.RDS_INSTANCE_BACKUP_DISABLED, RDSRules.RDS_INSTANCE_SHORT_BACKUP_RETENTION_PERIOD,
             RDSRules.RDS_INSTANCE_SINGLE_AZ, S3Rules.S3_BUCKET_NO_MFA_DELETE, S3Rules.S3_BUCKET_NO_VERSIONING,
             ELBv2Rules.ELBV2_NO_DELETION_PROTECTION]

    test = zero_trust_consts.TEST_SCOUTSUITE_DATA_LOSS_PREVENTION


class SecureAuthentication(ScoutSuiteFindingMap):
    rules = [
        IAMRules.IAM_USER_NO_ACTIVE_KEY_ROTATION,
        IAMRules.IAM_PASSWORD_POLICY_MINIMUM_LENGTH,
        IAMRules.IAM_PASSWORD_POLICY_NO_EXPIRATION,
        IAMRules.IAM_PASSWORD_POLICY_REUSE_ENABLED,
        IAMRules.IAM_USER_WITH_PASSWORD_AND_KEY,
        IAMRules.IAM_ASSUME_ROLE_LACKS_EXTERNAL_ID_AND_MFA,
        IAMRules.IAM_USER_WITHOUT_MFA,
        IAMRules.IAM_ROOT_ACCOUNT_NO_MFA,
        IAMRules.IAM_ROOT_ACCOUNT_WITH_ACTIVE_KEYS,
        IAMRules.IAM_USER_NO_INACTIVE_KEY_ROTATION,
        IAMRules.IAM_USER_WITH_MULTIPLE_ACCESS_KEYS
    ]

    test = zero_trust_consts.TEST_SCOUTSUITE_SECURE_AUTHENTICATION


class RestrictivePolicies(ScoutSuiteFindingMap):
    rules = [
        IAMRules.IAM_ASSUME_ROLE_POLICY_ALLOWS_ALL,
        IAMRules.IAM_EC2_ROLE_WITHOUT_INSTANCES,
        IAMRules.IAM_GROUP_WITH_INLINE_POLICIES,
        IAMRules.IAM_GROUP_WITH_NO_USERS,
        IAMRules.IAM_INLINE_GROUP_POLICY_ALLOWS_IAM_PASSROLE,
        IAMRules.IAM_INLINE_GROUP_POLICY_ALLOWS_NOTACTIONS,
        IAMRules.IAM_INLINE_GROUP_POLICY_ALLOWS_STS_ASSUMEROLE,
        IAMRules.IAM_INLINE_ROLE_POLICY_ALLOWS_IAM_PASSROLE,
        IAMRules.IAM_INLINE_ROLE_POLICY_ALLOWS_NOTACTIONS,
        IAMRules.IAM_INLINE_ROLE_POLICY_ALLOWS_STS_ASSUMEROLE,
        IAMRules.IAM_INLINE_USER_POLICY_ALLOWS_IAM_PASSROLE,
        IAMRules.IAM_INLINE_USER_POLICY_ALLOWS_NOTACTIONS,
        IAMRules.IAM_INLINE_USER_POLICY_ALLOWS_STS_ASSUMEROLE,
        IAMRules.IAM_MANAGED_POLICY_ALLOWS_IAM_PASSROLE,
        IAMRules.IAM_MANAGED_POLICY_ALLOWS_NOTACTIONS,
        IAMRules.IAM_MANAGED_POLICY_ALLOWS_STS_ASSUMEROLE,
        IAMRules.IAM_MANAGED_POLICY_NO_ATTACHMENTS,
        IAMRules.IAM_ROLE_WITH_INLINE_POLICIES,
        IAMRules.IAM_ROOT_ACCOUNT_USED_RECENTLY,
        IAMRules.IAM_ROOT_ACCOUNT_WITH_ACTIVE_CERTS,
        IAMRules.IAM_USER_WITH_INLINE_POLICIES,
        EC2Rules.AMI_PUBLIC,
        S3Rules.S3_BUCKET_AUTHENTICATEDUSERS_WRITE_ACP,
        S3Rules.S3_BUCKET_AUTHENTICATEDUSERS_WRITE,
        S3Rules.S3_BUCKET_AUTHENTICATEDUSERS_READ_ACP,
        S3Rules.S3_BUCKET_AUTHENTICATEDUSERS_READ,
        S3Rules.S3_BUCKET_ALLUSERS_WRITE_ACP,
        S3Rules.S3_BUCKET_ALLUSERS_WRITE,
        S3Rules.S3_BUCKET_ALLUSERS_READ_ACP,
        S3Rules.S3_BUCKET_ALLUSERS_READ,
        S3Rules.S3_BUCKET_WORLD_PUT_POLICY,
        S3Rules.S3_BUCKET_WORLD_POLICY_STAR,
        S3Rules.S3_BUCKET_WORLD_LIST_POLICY,
        S3Rules.S3_BUCKET_WORLD_GET_POLICY,
        S3Rules.S3_BUCKET_WORLD_DELETE_POLICY,
        EC2Rules.EC2_DEFAULT_SECURITY_GROUP_IN_USE,
        EC2Rules.EC2_DEFAULT_SECURITY_GROUP_WITH_RULES,
        EC2Rules.EC2_EBS_SNAPSHOT_PUBLIC,
        SQSRules.SQS_QUEUE_WORLD_SENDMESSAGE_POLICY,
        SQSRules.SQS_QUEUE_WORLD_RECEIVEMESSAGE_POLICY,
        SQSRules.SQS_QUEUE_WORLD_PURGEQUEUE_POLICY,
        SQSRules.SQS_QUEUE_WORLD_GETQUEUEURL_POLICY,
        SQSRules.SQS_QUEUE_WORLD_GETQUEUEATTRIBUTES_POLICY,
        SQSRules.SQS_QUEUE_WORLD_DELETEMESSAGE_POLICY,
        SQSRules.SQS_QUEUE_WORLD_CHANGEMESSAGEVISIBILITY_POLICY,
        SNSRules.SNS_TOPIC_WORLD_SUBSCRIBE_POLICY,
        SNSRules.SNS_TOPIC_WORLD_SETTOPICATTRIBUTES_POLICY,
        SNSRules.SNS_TOPIC_WORLD_REMOVEPERMISSION_POLICY,
        SNSRules.SNS_TOPIC_WORLD_RECEIVE_POLICY,
        SNSRules.SNS_TOPIC_WORLD_PUBLISH_POLICY,
        SNSRules.SNS_TOPIC_WORLD_DELETETOPIC_POLICY,
        SNSRules.SNS_TOPIC_WORLD_ADDPERMISSION_POLICY,
        SESRules.SES_IDENTITY_WORLD_SENDRAWEMAIL_POLICY,
        SESRules.SES_IDENTITY_WORLD_SENDEMAIL_POLICY,
        RedshiftRules.REDSHIFT_CLUSTER_PUBLICLY_ACCESSIBLE
    ]

    test = zero_trust_consts.TEST_SCOUTSUITE_RESTRICTIVE_POLICIES


class Logging(ScoutSuiteFindingMap):
    rules = [
        CloudTrailRules.CLOUDTRAIL_DUPLICATED_GLOBAL_SERVICES_LOGGING,
        CloudTrailRules.CLOUDTRAIL_NO_DATA_LOGGING,
        CloudTrailRules.CLOUDTRAIL_NO_GLOBAL_SERVICES_LOGGING,
        CloudTrailRules.CLOUDTRAIL_NO_LOG_FILE_VALIDATION,
        CloudTrailRules.CLOUDTRAIL_NO_LOGGING,
        CloudTrailRules.CLOUDTRAIL_NOT_CONFIGURED,
        CloudWatchRules.CLOUDWATCH_ALARM_WITHOUT_ACTIONS,
        ELBRules.ELB_NO_ACCESS_LOGS,
        S3Rules.S3_BUCKET_NO_LOGGING,
        ELBv2Rules.ELBV2_NO_ACCESS_LOGS,
        VPCRules.SUBNET_WITHOUT_FLOW_LOG,
        ConfigRules.CONFIG_RECORDER_NOT_CONFIGURED,
        RedshiftRules.REDSHIFT_PARAMETER_GROUP_LOGGING_DISABLED
    ]

    test = zero_trust_consts.TEST_SCOUTSUITE_LOGGING


class ServiceSecurity(ScoutSuiteFindingMap):
    rules = [
        CloudformationRules.CLOUDFORMATION_STACK_WITH_ROLE,
        ELBv2Rules.ELBV2_HTTP_REQUEST_SMUGGLING,
        RDSRules.RDS_INSTANCE_CA_CERTIFICATE_DEPRECATED,
        RDSRules.RDS_INSTANCE_NO_MINOR_UPGRADE,
        RedshiftRules.REDSHIFT_CLUSTER_NO_VERSION_UPGRADE
    ]

    test = zero_trust_consts.TEST_SCOUTSUITE_SERVICE_SECURITY
