import socket
from typing import Dict, Tuple

from common.common_consts.telem_categories import TelemCategoryEnum
from infection_monkey.i_puppet import PostBreachData
from infection_monkey.telemetry.base_telem import BaseTelem
from infection_monkey.utils.environment import is_windows_os


class PostBreachTelem(BaseTelem):

    telem_category = TelemCategoryEnum.POST_BREACH

    def __init__(self, post_breach_data: PostBreachData) -> None:
        super(PostBreachTelem, self).__init__()
        self.name = post_breach_data.display_name
        self.command = post_breach_data.command
        self.result = post_breach_data.result
        self.hostname, self.ip = PostBreachTelem._get_hostname_and_ip()

    def get_data(self) -> Dict:
        return {
            "command": self.command,
            "result": self.result,
            "name": self.name,
            "hostname": self.hostname,
            "ip": self.ip,
            "os": PostBreachTelem._get_os(),
        }

    @staticmethod
    def _get_hostname_and_ip() -> Tuple[str, str]:
        try:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
        except socket.error:
            hostname = "Unknown"
            ip = "Unknown"
        return hostname, ip

    @staticmethod
    def _get_os() -> str:
        return "Windows" if is_windows_os() else "Linux"
