import argparse
import pathlib
from typing import Type

from envs.monkey_zoo.blackbox.config_templates.config_template import ConfigTemplate
from envs.monkey_zoo.blackbox.config_templates.elastic import Elastic
from envs.monkey_zoo.blackbox.config_templates.hadoop import Hadoop
from envs.monkey_zoo.blackbox.config_templates.mssql import Mssql
from envs.monkey_zoo.blackbox.config_templates.performance import Performance
from envs.monkey_zoo.blackbox.config_templates.shellshock import ShellShock
from envs.monkey_zoo.blackbox.config_templates.smb_mimikatz import SmbMimikatz
from envs.monkey_zoo.blackbox.config_templates.smb_pth import SmbPth
from envs.monkey_zoo.blackbox.config_templates.ssh import Ssh
from envs.monkey_zoo.blackbox.config_templates.struts2 import Struts2
from envs.monkey_zoo.blackbox.config_templates.tunneling import Tunneling
from envs.monkey_zoo.blackbox.config_templates.weblogic import Weblogic
from envs.monkey_zoo.blackbox.config_templates.wmi_mimikatz import WmiMimikatz
from envs.monkey_zoo.blackbox.config_templates.wmi_pth import WmiPth
from envs.monkey_zoo.blackbox.config_templates.zerologon import Zerologon
from envs.monkey_zoo.blackbox.island_client.island_config_parser import IslandConfigParser
from envs.monkey_zoo.blackbox.island_client.monkey_island_client import MonkeyIslandClient

DST_DIR_NAME = 'generated_configs'
DST_DIR_PATH = pathlib.Path(pathlib.Path(__file__).parent.absolute(), DST_DIR_NAME)

parser = argparse.ArgumentParser(description='Generate config files.')
parser.add_argument('island_ip', metavar='IP:PORT',
                    help='Island endpoint. Example: 123.123.123.123:5000')

args = parser.parse_args()
island_client = MonkeyIslandClient(args.island_ip)


CONFIG_TEMPLATES = [
    Elastic,
    Hadoop,
    Mssql,
    Performance,
    ShellShock,
    SmbMimikatz,
    SmbPth,
    Ssh,
    Struts2,
    Tunneling,
    Weblogic,
    WmiMimikatz,
    WmiPth,
    Zerologon
]


def generate_templates():
    for template in CONFIG_TEMPLATES:
        save_template_as_config(template)


def save_template_as_config(template: Type[ConfigTemplate]):
    file_path = pathlib.Path(DST_DIR_PATH, f"{template.__name__}.conf")
    file_contents = IslandConfigParser.get_raw_config(template, island_client)
    save_to_file(file_path, file_contents)


def save_to_file(file_path, contents):
    with open(file_path, 'w') as file:
        file.write(contents)


if __name__ == '__main__':
    generate_templates()
