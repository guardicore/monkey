from monkey_island.cc.services.zero_trust.scoutsuite.consts.rule_names.rule_name_enum import RuleNameEnum


class SQSRules(RuleNameEnum):

    # Permissive policies
    SQS_QUEUE_WORLD_SENDMESSAGE_POLICY = 'sqs-queue-world-SendMessage-policy'
    SQS_QUEUE_WORLD_RECEIVEMESSAGE_POLICY = 'sqs-queue-world-ReceiveMessage-policy'
    SQS_QUEUE_WORLD_PURGEQUEUE_POLICY = 'sqs-queue-world-PurgeQueue-policy'
    SQS_QUEUE_WORLD_GETQUEUEURL_POLICY = 'sqs-queue-world-GetQueueUrl-policy'
    SQS_QUEUE_WORLD_GETQUEUEATTRIBUTES_POLICY = 'sqs-queue-world-GetQueueAttributes-policy'
    SQS_QUEUE_WORLD_DELETEMESSAGE_POLICY = 'sqs-queue-world-DeleteMessage-policy'
    SQS_QUEUE_WORLD_CHANGEMESSAGEVISIBILITY_POLICY = 'sqs-queue-world-ChangeMessageVisibility-policy'
