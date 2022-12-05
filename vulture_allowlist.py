from common import DIContainer
from common.agent_configuration import ScanTargetConfiguration
from common.agent_events import FileEncryptedEvent
from common.base_models import InfectionMonkeyModelConfig, MutableInfectionMonkeyModelConfig
from common.credentials import LMHash, NTHash, SecretEncodingConfig
from common.event_queue import QueuedAgentEventPublisher
from common.types import Event, Lock, NetworkPort
from infection_monkey.exploit.log4shell_utils.ldap_server import LDAPServerFactory
from infection_monkey.exploit.zerologon import NetrServerPasswordSet, NetrServerPasswordSetResponse
from infection_monkey.exploit.zerologon_utils.remote_shell import RemoteShell
from infection_monkey.island_api_client import HTTPIslandAPIClient
from infection_monkey.transport.http import FileServHTTPRequestHandler
from monkey_island.cc.deployment import Deployment
from monkey_island.cc.models import IslandMode, Machine
from monkey_island.cc.repositories import IAgentEventRepository, MongoAgentEventRepository
from monkey_island.cc.resources.agent_heartbeat import AgentHeartbeat
from monkey_island.cc.services.reporting.exploitations.monkey_exploitation import MonkeyExploitation
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
FileEncryptedEvent._file_path_to_pure_path

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

AWSCommandResults.response_code  # monkey_island/cc/services/aws/aws_command_runner.py:26

MonkeyExploitation.label

# Unused plugin infrastructure
HTTPIslandAPIClient.get_agent_plugin

# Remove after #2518
AgentHeartbeat

Lock.exc_type
Lock.exc_val
Lock.exc_tb
Lock.blocking
Lock.locked

# Remove after #2640
QueuedAgentEventPublisher
