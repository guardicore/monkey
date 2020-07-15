import logging

from monkey_island.cc.services.telemetry.processing.exploit import \
    process_exploit_telemetry
from monkey_island.cc.services.telemetry.processing.post_breach import \
    process_post_breach_telemetry
from monkey_island.cc.services.telemetry.processing.scan import \
    process_scan_telemetry
from monkey_island.cc.services.telemetry.processing.state import \
    process_state_telemetry
from monkey_island.cc.services.telemetry.processing.system_info import \
    process_system_info_telemetry
from monkey_island.cc.services.telemetry.processing.tunnel import \
    process_tunnel_telemetry

logger = logging.getLogger(__name__)

TELEMETRY_CATEGORY_TO_PROCESSING_FUNC = \
    {
        'tunnel': process_tunnel_telemetry,
        'state': process_state_telemetry,
        'exploit': process_exploit_telemetry,
        'scan': process_scan_telemetry,
        'system_info': process_system_info_telemetry,
        'post_breach': process_post_breach_telemetry,
        # `lambda *args, **kwargs: None` is a no-op.
        'trace': lambda *args, **kwargs: None,
        'attack': lambda *args, **kwargs: None,
    }


def process_telemetry(telemetry_json):
    try:
        telem_category = telemetry_json.get('telem_category')
        if telem_category in TELEMETRY_CATEGORY_TO_PROCESSING_FUNC:
            TELEMETRY_CATEGORY_TO_PROCESSING_FUNC[telem_category](telemetry_json)
        else:
            logger.info('Got unknown type of telemetry: %s' % telem_category)
    except Exception as ex:
        logger.error("Exception caught while processing telemetry. Info: {}".format(ex), exc_info=True)
