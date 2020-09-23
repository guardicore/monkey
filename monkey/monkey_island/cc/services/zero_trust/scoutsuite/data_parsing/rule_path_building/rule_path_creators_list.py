from monkey_island.cc.services.zero_trust.scoutsuite.data_parsing.rule_path_building.rule_path_creators.cloudtrail_rule_path_creator import \
    CloudTrailRulePathCreator
from monkey_island.cc.services.zero_trust.scoutsuite.data_parsing.rule_path_building.rule_path_creators.cloudwatch_rule_path_creator import \
    CloudWatchRulePathCreator
from monkey_island.cc.services.zero_trust.scoutsuite.data_parsing.rule_path_building.rule_path_creators.ec2_rule_path_creator import \
    EC2RulePathCreator
from monkey_island.cc.services.zero_trust.scoutsuite.data_parsing.rule_path_building.rule_path_creators.elb_rule_path_creator import \
    ELBRulePathCreator
from monkey_island.cc.services.zero_trust.scoutsuite.data_parsing.rule_path_building.rule_path_creators.elbv2_rule_path_creator import \
    ELBv2RulePathCreator
from monkey_island.cc.services.zero_trust.scoutsuite.data_parsing.rule_path_building.rule_path_creators.iam_rule_path_creator import \
    IAMRulePathCreator
from monkey_island.cc.services.zero_trust.scoutsuite.data_parsing.rule_path_building.rule_path_creators.rds_rule_path_creator import \
    RDSRulePathCreator
from monkey_island.cc.services.zero_trust.scoutsuite.data_parsing.rule_path_building.rule_path_creators.redshift_rule_path_creator import \
    RedshiftRulePathCreator
from monkey_island.cc.services.zero_trust.scoutsuite.data_parsing.rule_path_building.rule_path_creators.s3_rule_path_creator import \
    S3RulePathCreator
from monkey_island.cc.services.zero_trust.scoutsuite.data_parsing.rule_path_building.rule_path_creators.vpc_rule_path_creator import \
    VPCRulePathCreator

RULE_PATH_CREATORS_LIST = [EC2RulePathCreator, ELBv2RulePathCreator, RDSRulePathCreator, RedshiftRulePathCreator,
                           S3RulePathCreator, IAMRulePathCreator, CloudTrailRulePathCreator, ELBRulePathCreator,
                           VPCRulePathCreator, CloudWatchRulePathCreator]
