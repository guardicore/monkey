from enum import Enum


SERVICES = 'services'
FINDINGS = 'findings'


class SERVICE_TYPES(Enum):
    ACM = 'acm'
    AWSLAMBDA = 'awslambda'
    CLOUDFORMATION = 'cloudformation'
    CLOUSDTRAIL = 'cloudtrail'
    CLOUDWATCH = 'cloudwatch'
    CONFIG = 'config'
    DIRECTCONNECT = 'directconnect'
    EC2 = 'ec2'
    EFS = 'efs'
    ELASTICACHE = 'elasticache'
    ELB = 'elb'
    ELBv2 = 'elbv2'
    EMR = 'emr'
    IAM = 'iam'
    KMS = 'kms'
    RDS = 'rds'
    REDSHIFT = 'redshift'
    ROUTE53 = 'route53'
    S3 = 's3'
    SES = 'ses'
    SNS = 'sns'
    SQS = 'sqs'
    VPC = 'vpc'
    SECRETSMANAGER = 'secretsmanager'
