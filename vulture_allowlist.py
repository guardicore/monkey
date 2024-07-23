from agent_plugins.credentials_collectors.chrome.utils import BrowserCredentialsDatabasePath
from agent_plugins.exploiters.powershell.src.powershell_remote_access_client import (
    PowerShellRemoteAccessClient,
)
from agent_plugins.exploiters.snmp.src.snmp_exploit_client import SNMPResult
from agent_plugins.exploiters.zerologon.src.HostExploiter import HostExploiter
from agent_plugins.payloads.cryptojacker.src import cpu_utilizer, cryptojacker, memory_utilizer
from agent_plugins.payloads.ransomware.src.plugin import Plugin as RansomwarePlugin
from agent_plugins.payloads.ransomware.src.ransomware_options import (
    EncryptionBehavior,
    RansomwareOptions,
    linux_target_dir,
    windows_target_dir,
)
from flask_security import Security

from common.agent_configuration import ScanTargetConfiguration
from common.agent_plugins import (
    AgentPlugin,
    AgentPluginManifest,
    AgentPluginMetadata,
    AgentPluginRepositoryIndex,
)
from infection_monkey.command_builders import (
    AgentCommandBuilderFactory,
    LinuxAgentCommandBuilder,
    WindowsAgentCommandBuilder,
)
from infection_monkey.exploit.log4shell_utils.ldap_server import LDAPServerFactory
from infection_monkey.exploit.tools import secret_type_filter
from infection_monkey.exploit.zerologon import NetrServerPasswordSet, NetrServerPasswordSetResponse
from infection_monkey.exploit.zerologon_utils.remote_shell import RemoteShell
from infection_monkey.network.firewall import FirewallApp, WinAdvFirewall, WinFirewall
from infection_monkey.utils import commands
from monkey_island.cc.deployment import Deployment
from monkey_island.cc.models import Machine
from monkey_island.cc.repositories import IAgentEventRepository, MongoAgentEventRepository
from monkey_island.cc.services.agent_plugin_service import AgentPluginService
from monkey_island.cc.services.authentication_service.user import User
from monkey_island.cc.services.reporting.exploitations.monkey_exploitation import MonkeyExploitation

# Pydantic configurations are not picked up
ScanTargetConfiguration.blocked_ips_valid
ScanTargetConfiguration.inaccessible_subnets
ScanTargetConfiguration.subnets_valid
ScanTargetConfiguration.inaccessible_subnets_valid


LMHash.validate_hash_format
NTHash.validate_hash_format


AgentPluginManifest.title
AgentPluginManifest.description
AgentPluginManifest.link_to_documentation
AgentPluginManifest.safe
AgentPluginManifest.remediation_suggestion
AgentPluginManifest.target_operating_systems
AgentPluginManifest.supported_operating_systems

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

# Zerologon uses this to restore password:
RemoteShell.do_get
RemoteShell.do_exit
prompt

FirewallApp.listen_allowed
WinAdvFirewall.listen_allowed
WinFirewall.listen_allowed

# Server configurations
app.url_map.strict_slashes
api.representations
hub.exception_stream
app.login_via_request
app.should_set_cookie
app.session_interface
app.save_session
Security._want_json

# Deployment is chosen dynamically
Deployment.DEVELOP
Deployment.APPIMAGE
Deployment.DOCKER

# Pydantic models
Machine._socketaddress_from_string
Machine.dump_network_services
# Unused, but potentially useful
Machine.island

# We anticipate using these in the future
IAgentEventRepository.get_events_by_tag
IAgentEventRepository.get_events_by_source
MongoAgentEventRepository.get_events_by_tag
MongoAgentEventRepository.get_events_by_source

AWSCommandResults.response_code  # monkey_island/cc/services/aws/aws_command_runner.py:26

MonkeyExploitation.label

AgentPlugin.dump_source_archive
AgentPlugin.supported_operating_systems

BrowserCredentialsDatabasePath.database_file_path

HostExploiter.add_vuln_url

EncryptionBehavior.validate_file_extension
EncryptionBehavior.validate_linux_target_dir
EncryptionBehavior.validate_windows_target_dir
RansomwareOptions.encryption
RansomwareOptions.other_behaviors
linux_target_dir
windows_target_dir


# User model fields
User.active
User.fs_uniquifier
User.roles
User.get_by_id
User.email

identity_type_filter
secret_type_filter

SNMPResult.errorIndex
SNMPResult.varBinds

commands.build_agent_deploy_command
commands.build_agent_download_command
commands.build_command_windows_powershell
commands.build_download_command_linux_curl
commands.build_dropper_script_download_command
commands.build_download_command_windows_powershell_webclient
commands.build_download_command_windows_powershell_webrequest

# Remove after the plugin interface is in place
AgentPluginMetadata.resource_path
AgentPluginMetadata._str_to_pure_posix_path
AgentPluginMetadata.model_config
AgentPluginMetadata.dump_string
AgentPluginRepositoryIndex
AgentPluginRepositoryIndex.model_config
AgentPluginRepositoryIndex.dump_compatible_infection_monkey_version
AgentPluginRepositoryIndex.compatible_infection_monkey_version
AgentPluginRepositoryIndex._infection_monkey_version_parser
AgentPluginRepositoryIndex._sort_plugins_by_version
AgentPluginRepositoryIndex.use_enum_values
AgentPluginRepositoryIndex._convert_str_type_to_enum

AgentPluginService.install_agent_plugin_from_repository

# TODO: Remove after we move the plugins to separate repos
execute_agent
LinuxAgentCommandBuilder.build_permission_change_command

RansomwarePlugin

PowerShellRemoteAccessClient.get_writable_paths
