from monkey_island.cc.services.config_schema.basic import BASIC
from monkey_island.cc.services.config_schema.basic_network import BASIC_NETWORK
from monkey_island.cc.services.config_schema.definitions.credential_collector_classes import (
    CREDENTIAL_COLLECTOR_CLASSES,
)
from monkey_island.cc.services.config_schema.definitions.exploiter_classes import EXPLOITER_CLASSES
from monkey_island.cc.services.config_schema.definitions.finger_classes import FINGER_CLASSES
from monkey_island.cc.services.config_schema.definitions.post_breach_actions import (
    POST_BREACH_ACTIONS,
)
from monkey_island.cc.services.config_schema.internal import INTERNAL
from monkey_island.cc.services.config_schema.monkey import MONKEY
from monkey_island.cc.services.config_schema.ransomware import RANSOMWARE

SCHEMA = {
    "title": "Monkey",
    "type": "object",
    # Newly added definitions should also be added to
    # monkey/monkey_island/cc/ui/src/components/utils/SafeOptionValidator.js so that
    # users will not accidentally chose unsafe options
    "definitions": {
        "exploiter_classes": EXPLOITER_CLASSES,
        "credential_collector_classes": CREDENTIAL_COLLECTOR_CLASSES,
        "post_breach_actions": POST_BREACH_ACTIONS,
        "finger_classes": FINGER_CLASSES,
    },
    "properties": {
        "basic": BASIC,
        "basic_network": BASIC_NETWORK,
        "monkey": MONKEY,
        "ransomware": RANSOMWARE,
        "internal": INTERNAL,
    },
    "options": {"collapsed": True},
}
