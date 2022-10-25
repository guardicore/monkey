import logging

from common.agent_configuration import AgentConfiguration
from common.common_consts.telem_categories import TelemCategoryEnum
from monkey_island.cc.models.telemetries import save_telemetry
from monkey_island.cc.services.telemetry.processing.aws_info import process_aws_telemetry
from monkey_island.cc.services.telemetry.processing.state import process_state_telemetry

logger = logging.getLogger(__name__)

TELEMETRY_CATEGORY_TO_PROCESSING_FUNC = {
    TelemCategoryEnum.AWS_INFO: process_aws_telemetry,
    TelemCategoryEnum.STATE: process_state_telemetry,
    # `lambda *args, **kwargs: None` is a no-op.
    TelemCategoryEnum.TRACE: lambda *args, **kwargs: None,
}


def process_telemetry(telemetry_json, agent_configuration: AgentConfiguration):
    try:
        telem_category = telemetry_json.get("telem_category")
        if telem_category in TELEMETRY_CATEGORY_TO_PROCESSING_FUNC:
            TELEMETRY_CATEGORY_TO_PROCESSING_FUNC[telem_category](
                telemetry_json, agent_configuration
            )
        else:
            logger.info("Got unknown type of telemetry: %s" % telem_category)

        save_telemetry(telemetry_json)

    except Exception as ex:
        logger.error(
            "Exception caught while processing telemetry. Info: {}".format(ex), exc_info=True
        )
