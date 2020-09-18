from enum import Enum


class EC2Rules(Enum):
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
