from agent_plugins.exploiters.hadoop.plugin import Plugin as HadoopPlugin

from common import DIContainer
from common.agent_configuration import ScanTargetConfiguration
from common.agent_events import AbstractAgentEvent, FileEncryptionEvent
from common.agent_plugins import AgentPlugin, AgentPluginManifest
from common.base_models import InfectionMonkeyModelConfig, MutableInfectionMonkeyModelConfig
from common.credentials import LMHash, NTHash, SecretEncodingConfig
from common.hard_coded_manifests import HARD_CODED_PAYLOADS_MANIFESTS
from common.hard_coded_manifests.hard_coded_credential_collector_manifests import (
    HARD_CODED_CREDENTIAL_COLLECTOR_MANIFESTS,
)
from common.hard_coded_manifests.hard_coded_fingerprinter_manifests import (
    HARD_CODED_FINGERPRINTER_MANIFESTS,
)
from common.types import Lock, NetworkPort, NetworkService, PluginName
from infection_monkey.exploit.log4shell_utils.ldap_server import LDAPServerFactory
from infection_monkey.exploit.zerologon import NetrServerPasswordSet, NetrServerPasswordSetResponse
from infection_monkey.exploit.zerologon_utils.remote_shell import RemoteShell
from infection_monkey.transport.http import FileServHTTPRequestHandler
from monkey_island.cc.deployment import Deployment
from monkey_island.cc.models import IslandMode, Machine, Role, User
from monkey_island.cc.repositories import IAgentEventRepository, MongoAgentEventRepository
from monkey_island.cc.repositories.utils.hard_coded_credential_collector_schemas import (
    HARD_CODED_CREDENTIAL_COLLECTOR_SCHEMAS,
)
from monkey_island.cc.repositories.utils.hard_coded_fingerprinter_schemas import (
    HARD_CODED_FINGERPRINTER_SCHEMAS,
)
from monkey_island.cc.repositories.utils.hard_coded_payloads_schemas import (
    HARD_CODED_PAYLOADS_SCHEMAS,
)
from monkey_island.cc.services.reporting.exploitations.monkey_exploitation import MonkeyExploitation

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

PluginName.strip_whitespace
PluginName.regex

SecretEncodingConfig.json_encoders

LMHash.validate_hash_format
NTHash.validate_hash_format

NetworkPort.ge
NetworkPort.le

FileEncryptionEvent.arbitrary_types_allowed
FileEncryptionEvent._file_path_to_pure_path

AbstractAgentEvent.smart_union

AgentPluginManifest.title
AgentPluginManifest.description
AgentPluginManifest.link_to_documentation
AgentPluginManifest.safe
AgentPluginManifest.remediation_suggestion
AgentPluginManifest.target_operating_systems
AgentPluginManifest.supported_operating_systems

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

# Attribute used by pydantic errors
msg_template

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

# Server configurations
app.url_map.strict_slashes
api.representations
hub.exception_stream

# Deployment is chosen dynamically
Deployment.DEVELOP
Deployment.APPIMAGE
Deployment.DOCKER

# Pydantic models
Machine.Config.json_dumps
Machine._socketaddress_from_string
# Unused, but potentially useful
Machine.island

IslandMode.ADVANCED

# We anticipate using these in the future
IAgentEventRepository.get_events_by_tag
IAgentEventRepository.get_events_by_source
MongoAgentEventRepository.get_events_by_tag
MongoAgentEventRepository.get_events_by_source

AWSCommandResults.response_code  # monkey_island/cc/services/aws/aws_command_runner.py:26

MonkeyExploitation.label

Lock.exc_type
Lock.exc_val
Lock.exc_tb
Lock.blocking
Lock.locked

AgentPlugin.supported_operating_systems

HadoopPlugin

# Remove after #2136
NetworkService.HTTP
NetworkService.MSSQL
NetworkService.SMB

# Remove after #2750
HARD_CODED_CREDENTIAL_COLLECTOR_SCHEMAS
HARD_CODED_FINGERPRINTER_SCHEMAS
HARD_CODED_CREDENTIAL_COLLECTOR_MANIFESTS
HARD_CODED_FINGERPRINTER_MANIFESTS
HARD_CODED_PAYLOADS_MANIFESTS
HARD_CODED_PAYLOADS_SCHEMAS

# Remove after #2157
User.active
User.fs_uniquifier
User.roles
User.get_by_id
Role.permissions
