from common import DIContainer
from common.agent_configuration import ScanTargetConfiguration
from common.agent_events import FileEncryptedEvent
from common.base_models import InfectionMonkeyModelConfig, MutableInfectionMonkeyModelConfig
from common.credentials import LMHash, NTHash, SecretEncodingConfig
from common.types import NetworkPort
from infection_monkey.exploit.log4shell_utils.ldap_server import LDAPServerFactory
from infection_monkey.exploit.zerologon import NetrServerPasswordSet, NetrServerPasswordSetResponse
from infection_monkey.exploit.zerologon_utils.remote_shell import RemoteShell
from infection_monkey.transport.http import FileServHTTPRequestHandler
from monkey_island.cc.deployment import Deployment
from monkey_island.cc.models import IslandMode, Machine, Monkey, MonkeyTtl, Report
from monkey_island.cc.models.edge import Edge
from monkey_island.cc.repository import IAgentEventRepository, MongoAgentEventRepository
from monkey_island.cc.services.reporting.issue_processing.exploit_processing.exploiter_descriptor_enum import (
    ExploiterDescriptorEnum,
)

# Pydantic configurations are not picked up
ScanTargetConfiguration.blocked_ips_valid
ScanTargetConfiguration.inaccessible_subnets
ScanTargetConfiguration.subnets_valid
ScanTargetConfiguration.inaccessible_subnets_valid

InfectionMonkeyModelConfig.allow_mutation
InfectionMonkeyModelConfig.underscore_attrs_are_private
InfectionMonkeyModelConfig.extra

MutableInfectionMonkeyModelConfig.allow_mutation
MutableInfectionMonkeyModelConfig.validate_assignment

SecretEncodingConfig.json_encoders

LMHash.validate_hash_format
NTHash.validate_hash_format

NetworkPort.ge
NetworkPort.le

FileEncryptedEvent.arbitrary_types_allowed
# TODO: Remove after #2496
FileEncryptedEvent

# Unused, but kept for future potential
DIContainer.release_convention

# Used by third party library
LDAPServerFactory.buildProtocol
NetrServerPasswordSet.structure
NetrServerPasswordSetResponse.structure
NetrServerPasswordSet.opnum

# Passed to Popen from agent
dwFlags  # \infection_monkey\monkey\infection_monkey\monkey.py:490:
wShowWindow  # \infection_monkey\monkey\infection_monkey\monkey.py:491:

# Presumably overrides http.server.BaseHTTPRequestHandler properties
FileServHTTPRequestHandler.protocol_version
FileServHTTPRequestHandler.version_string
FileServHTTPRequestHandler.close_connection
FileServHTTPRequestHandler.do_POST
FileServHTTPRequestHandler.do_GET
FileServHTTPRequestHandler.do_HEAD

# Zerologon uses this to restore password:
RemoteShell.do_get
RemoteShell.do_exit
prompt

agent.stop_time  # \monkey\monkey_island\cc\agent_event_handlers\update_agent_shutdown_status.py:17: unused attribute 'stop_time'

# Server configurations
app.url_map.strict_slashes
api.representations
hub.exception_stream

# Deployment is chosen dynamically
Deployment.DEVELOP
Deployment.APPIMAGE
Deployment.DOCKER

# Mongoengine documents
Edge.meta
Monkey.guid
Monkey.launch_time
MonkeyTtl.expire_at
Report.overview
Report.glance
Report.recommendations
Report.meta_info

# Pymongo models
Machine.Config.json_dumps
Machine._socketaddress_from_string
# Maybe we'll use this later
Machine.operating_system_version

IslandMode.ADVANCED

# We anticipate using these in the future
IAgentEventRepository.get_events_by_tag
IAgentEventRepository.get_events_by_source
MongoAgentEventRepository.get_events_by_tag
MongoAgentEventRepository.get_events_by_source

# ExploiterDescriptorEnum
ExploiterDescriptorEnum.SMB
ExploiterDescriptorEnum.WMI
ExploiterDescriptorEnum.SSH
ExploiterDescriptorEnum.HADOOP
ExploiterDescriptorEnum.MSSQL
ExploiterDescriptorEnum.POWERSHELL
ExploiterDescriptorEnum.LOG4SHELL

# Remove when Database service is removed
Database._should_drop.drop_config  # monkey_island/cc/services/database.py:28

AWSCommandResults.response_code  # monkey_island/cc/services/aws/aws_command_runner.py:26
