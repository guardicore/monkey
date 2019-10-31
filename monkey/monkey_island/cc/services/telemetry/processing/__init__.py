# import all implemented hooks, for brevity of hooks.py file
from .tunnel import process_tunnel_telemetry
from .state import process_state_telemetry
from .exploit import process_exploit_telemetry
from .scan import process_scan_telemetry
from .system_info import process_system_info_telemetry
from .post_breach import process_post_breach_telemetry
