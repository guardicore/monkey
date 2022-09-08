import logging

from common.agent_configuration import AgentConfiguration
from common.common_consts.telem_categories import TelemCategoryEnum
from monkey_island.cc.models.telemetries import save_telemetry
from monkey_island.cc.services.telemetry.processing.aws_info import process_aws_telemetry
from monkey_island.cc.services.telemetry.processing.exploit import process_exploit_telemetry
from monkey_island.cc.services.telemetry.processing.post_breach import process_post_breach_telemetry
from monkey_island.cc.services.telemetry.processing.scan import process_scan_telemetry
from monkey_island.cc.services.telemetry.processing.state import process_state_telemetry

logger = logging.getLogger(__name__)

TELEMETRY_CATEGORY_TO_PROCESSING_FUNC = {
    # `lambda *args, **kwargs: None` is a no-op.
    TelemCategoryEnum.ATTACK: lambda *args, **kwargs: None,
    TelemCategoryEnum.AWS_INFO: process_aws_telemetry,
    TelemCategoryEnum.CREDENTIALS: None,  # this is set in monkey_island/cc/services/initialize.py
    TelemCategoryEnum.EXPLOIT: process_exploit_telemetry,
    TelemCategoryEnum.POST_BREACH: process_post_breach_telemetry,
    TelemCategoryEnum.SCAN: process_scan_telemetry,
    TelemCategoryEnum.STATE: process_state_telemetry,
    TelemCategoryEnum.TRACE: lambda *args, **kwargs: None,
}

# Don't save credential telemetries in telemetries collection.
# Credentials are stored in StolenCredentials documents
UNSAVED_TELEMETRIES = [TelemCategoryEnum.CREDENTIALS]


def process_telemetry(telemetry_json, agent_configuration: AgentConfiguration):
    try:
        telem_category = telemetry_json.get("telem_category")
        if telem_category in TELEMETRY_CATEGORY_TO_PROCESSING_FUNC:
            TELEMETRY_CATEGORY_TO_PROCESSING_FUNC[telem_category](
                telemetry_json, agent_configuration
            )
        else:
            logger.info("Got unknown type of telemetry: %s" % telem_category)

        if telem_category not in UNSAVED_TELEMETRIES:
            save_telemetry(telemetry_json)

    except Exception as ex:
        logger.error(
            "Exception caught while processing telemetry. Info: {}".format(ex), exc_info=True
        )
