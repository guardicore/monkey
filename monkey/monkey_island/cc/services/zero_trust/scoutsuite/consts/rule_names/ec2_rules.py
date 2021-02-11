from monkey_island.cc.services.zero_trust.scoutsuite.consts.rule_names.rule_name_enum import RuleNameEnum


class EC2Rules(RuleNameEnum):
    # Permissive firewall rules
    SECURITY_GROUP_ALL_PORTS_TO_ALL = 'ec2-security-group-opens-all-ports-to-all'
    SECURITY_GROUP_OPENS_TCP_PORT_TO_ALL = 'ec2-security-group-opens-TCP-port-to-all'
    SECURITY_GROUP_OPENS_UDP_PORT_TO_ALL = 'ec2-security-group-opens-UDP-port-to-all'
    SECURITY_GROUP_OPENS_RDP_PORT_TO_ALL = 'ec2-security-group-opens-RDP-port-to-all'
    SECURITY_GROUP_OPENS_SSH_PORT_TO_ALL = 'ec2-security-group-opens-SSH-port-to-all'
    SECURITY_GROUP_OPENS_MYSQL_PORT_TO_ALL = 'ec2-security-group-opens-MySQL-port-to-all'
    SECURITY_GROUP_OPENS_MSSQL_PORT_TO_ALL = 'ec2-security-group-opens-MsSQL-port-to-all'
    SECURITY_GROUP_OPENS_MONGODB_PORT_TO_ALL = 'ec2-security-group-opens-MongoDB-port-to-all'
    SECURITY_GROUP_OPENS_ORACLE_DB_PORT_TO_ALL = 'ec2-security-group-opens-Oracle DB-port-to-all'
    SECURITY_GROUP_OPENS_POSTGRESQL_PORT_TO_ALL = 'ec2-security-group-opens-PostgreSQL-port-to-all'
    SECURITY_GROUP_OPENS_NFS_PORT_TO_ALL = 'ec2-security-group-opens-NFS-port-to-all'
    SECURITY_GROUP_OPENS_SMTP_PORT_TO_ALL = 'ec2-security-group-opens-SMTP-port-to-all'
    SECURITY_GROUP_OPENS_DNS_PORT_TO_ALL = 'ec2-security-group-opens-DNS-port-to-all'
    SECURITY_GROUP_OPENS_ALL_PORTS_TO_SELF = 'ec2-security-group-opens-all-ports-to-self'
    SECURITY_GROUP_OPENS_ALL_PORTS = 'ec2-security-group-opens-all-ports'
    SECURITY_GROUP_OPENS_PLAINTEXT_PORT_FTP = 'ec2-security-group-opens-plaintext-port-FTP'
    SECURITY_GROUP_OPENS_PLAINTEXT_PORT_TELNET = 'ec2-security-group-opens-plaintext-port-Telnet'
    SECURITY_GROUP_OPENS_PORT_RANGE = 'ec2-security-group-opens-port-range'
    EC2_SECURITY_GROUP_WHITELISTS_AWS = 'ec2-security-group-whitelists-aws'

    # Encryption
    EBS_SNAPSHOT_NOT_ENCRYPTED = 'ec2-ebs-snapshot-not-encrypted'
    EBS_VOLUME_NOT_ENCRYPTED = 'ec2-ebs-volume-not-encrypted'
    EC2_INSTANCE_WITH_USER_DATA_SECRETS = 'ec2-instance-with-user-data-secrets'

    # Permissive policies
    AMI_PUBLIC = 'ec2-ami-public'
    EC2_DEFAULT_SECURITY_GROUP_IN_USE = 'ec2-default-security-group-in-use'
    EC2_DEFAULT_SECURITY_GROUP_WITH_RULES = 'ec2-default-security-group-with-rules'
    EC2_EBS_SNAPSHOT_PUBLIC = 'ec2-ebs-snapshot-public'
