import logging

from common.common_consts.telem_categories import TelemCategoryEnum
from infection_monkey.telemetry.base_telem import BaseTelem

__author__ = "itay.mizeretz"

LOG = logging.getLogger(__name__)


class TraceTelem(BaseTelem):

    def __init__(self, msg):
        """
        Default trace telemetry constructor
        :param msg: Trace message
        """
        super(TraceTelem, self).__init__()
        self.msg = msg
        LOG.debug("Trace: %s" % msg)

    telem_category = TelemCategoryEnum.TRACE

    def get_data(self):
        return {
            'msg': self.msg
        }
