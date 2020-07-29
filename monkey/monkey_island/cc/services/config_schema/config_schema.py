from monkey_island.cc.services.config_schema.basic import BASIC
from monkey_island.cc.services.config_schema.basic_network import BASIC_NETWORK
from monkey_island.cc.services.config_schema.definitions.exploiter_classes import \
    EXPLOITER_CLASSES
from monkey_island.cc.services.config_schema.definitions.finger_classes import \
    FINGER_CLASSES
from monkey_island.cc.services.config_schema.definitions.post_breach_actions import \
    POST_BREACH_ACTIONS
from monkey_island.cc.services.config_schema.definitions.system_info_collector_classes import \
    SYSTEM_INFO_COLLECTOR_CLASSES
from monkey_island.cc.services.config_schema.internal import INTERNAL
from monkey_island.cc.services.config_schema.monkey import MONKEY

SCHEMA = {
    "title": "Monkey",
    "type": "object",
    "definitions": {
        "exploiter_classes": EXPLOITER_CLASSES,
        "system_info_collector_classes": SYSTEM_INFO_COLLECTOR_CLASSES,
        "post_breach_actions": POST_BREACH_ACTIONS,
        "finger_classes": FINGER_CLASSES

    },
    "properties": {
        "basic": BASIC,
        "basic_network": BASIC_NETWORK,
        "monkey": MONKEY,
        "internal": INTERNAL,
    },
    "options": {
        "collapsed": True
    }
}
