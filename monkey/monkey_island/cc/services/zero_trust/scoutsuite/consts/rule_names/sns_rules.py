from monkey_island.cc.services.zero_trust.scoutsuite.consts.rule_names.rule_name_enum import RuleNameEnum


class SNSRules(RuleNameEnum):

    # Permissive policies
    SNS_TOPIC_WORLD_SUBSCRIBE_POLICY = 'sns-topic-world-Subscribe-policy'
    SNS_TOPIC_WORLD_SETTOPICATTRIBUTES_POLICY = 'sns-topic-world-SetTopicAttributes-policy'
    SNS_TOPIC_WORLD_REMOVEPERMISSION_POLICY = 'sns-topic-world-RemovePermission-policy'
    SNS_TOPIC_WORLD_RECEIVE_POLICY = 'sns-topic-world-Receive-policy'
    SNS_TOPIC_WORLD_PUBLISH_POLICY = 'sns-topic-world-Publish-policy'
    SNS_TOPIC_WORLD_DELETETOPIC_POLICY = 'sns-topic-world-DeleteTopic-policy'
    SNS_TOPIC_WORLD_ADDPERMISSION_POLICY = 'sns-topic-world-AddPermission-policy'
