from monkey_island.cc.services.telemetry.processing import *

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
