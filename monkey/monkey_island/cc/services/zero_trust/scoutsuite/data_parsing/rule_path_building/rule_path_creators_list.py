from monkey_island.cc.services.zero_trust.scoutsuite.data_parsing.rule_path_building.rule_path_creators.cloudformation_rule_path_creator import ( # noqa: E501
    CloudformationRulePathCreator,
)
from monkey_island.cc.services.zero_trust.scoutsuite.data_parsing.rule_path_building.rule_path_creators.cloudtrail_rule_path_creator import (  # noqa: E501
    CloudTrailRulePathCreator,
)
from monkey_island.cc.services.zero_trust.scoutsuite.data_parsing.rule_path_building.rule_path_creators.cloudwatch_rule_path_creator import ( # noqa: E501
    CloudWatchRulePathCreator,
)
from monkey_island.cc.services.zero_trust.scoutsuite.data_parsing.rule_path_building.rule_path_creators.config_rule_path_creator import ( # noqa: E501
    ConfigRulePathCreator,
)
from monkey_island.cc.services.zero_trust.scoutsuite.data_parsing.rule_path_building.rule_path_creators.ec2_rule_path_creator import ( # noqa: E501
    EC2RulePathCreator,
)
from monkey_island.cc.services.zero_trust.scoutsuite.data_parsing.rule_path_building.rule_path_creators.elb_rule_path_creator import ( # noqa: E501
    ELBRulePathCreator,
)
from monkey_island.cc.services.zero_trust.scoutsuite.data_parsing.rule_path_building.rule_path_creators.elbv2_rule_path_creator import ( # noqa: E501
    ELBv2RulePathCreator,
)
from monkey_island.cc.services.zero_trust.scoutsuite.data_parsing.rule_path_building.rule_path_creators.iam_rule_path_creator import ( # noqa: E501
    IAMRulePathCreator,
)
from monkey_island.cc.services.zero_trust.scoutsuite.data_parsing.rule_path_building.rule_path_creators.rds_rule_path_creator import ( # noqa: E501
    RDSRulePathCreator,
)
from monkey_island.cc.services.zero_trust.scoutsuite.data_parsing.rule_path_building.rule_path_creators.redshift_rule_path_creator import ( # noqa: E501
    RedshiftRulePathCreator,
)
from monkey_island.cc.services.zero_trust.scoutsuite.data_parsing.rule_path_building.rule_path_creators.s3_rule_path_creator import ( # noqa: E501
    S3RulePathCreator,
)
from monkey_island.cc.services.zero_trust.scoutsuite.data_parsing.rule_path_building.rule_path_creators.ses_rule_path_creator import ( # noqa: E501
    SESRulePathCreator,
)
from monkey_island.cc.services.zero_trust.scoutsuite.data_parsing.rule_path_building.rule_path_creators.sns_rule_path_creator import ( # noqa: E501
    SNSRulePathCreator,
)
from monkey_island.cc.services.zero_trust.scoutsuite.data_parsing.rule_path_building.rule_path_creators.sqs_rule_path_creator import ( # noqa: E501
    SQSRulePathCreator,
)
from monkey_island.cc.services.zero_trust.scoutsuite.data_parsing.rule_path_building.rule_path_creators.vpc_rule_path_creator import ( # noqa: E501
    VPCRulePathCreator,
)

RULE_PATH_CREATORS_LIST = [
    EC2RulePathCreator,
    ELBv2RulePathCreator,
    RDSRulePathCreator,
    RedshiftRulePathCreator,
    S3RulePathCreator,
    IAMRulePathCreator,
    CloudTrailRulePathCreator,
    ELBRulePathCreator,
    VPCRulePathCreator,
    CloudWatchRulePathCreator,
    SQSRulePathCreator,
    SNSRulePathCreator,
    SESRulePathCreator,
    ConfigRulePathCreator,
    CloudformationRulePathCreator,
]
