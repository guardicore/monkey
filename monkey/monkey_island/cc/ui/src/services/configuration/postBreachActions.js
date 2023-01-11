const POST_BREACH_ACTIONS = {
  'title': 'Post-Breach Actions',
  'description': 'This action safely simulates what a person might do after breaching a new machine. Used in ATT&CK and Zero Trust reports.',
  'type': 'string',
  'pluginDefs': {
    'CommunicateAsBackdoorUser':{'name': 'CommunicateAsBackdoorUser', 'options':{}},
    'ModifyShellStartupFiles':{'name': 'ModifyShellStartupFiles', 'options':{}},
    'HiddenFiles':{'name': 'HiddenFiles', 'options':{}},
    'TrapCommand':{'name': 'TrapCommand', 'options':{}},
    'ChangeSetuidSetgid':{'name': 'ChangeSetuidSetgid', 'options':{}},
    'ScheduleJobs':{'name': 'ScheduleJobs', 'options':{}},
    'Timestomping':{'name': 'Timestomping', 'options':{}},
    'SignedScriptProxyExecution':{'name': 'SignedScriptProxyExecution', 'options':{}},
    'AccountDiscovery':{'name': 'AccountDiscovery', 'options':{}},
    'ClearCommandHistory':{'name': 'ClearCommandHistory', 'options':{}},
    'ProcessListCollection':{'name': 'ProcessListCollection', 'options':{}}
  },
  'anyOf': [
    {
      'type': 'string',
      'enum': ['CommunicateAsBackdoorUser'],
      'title': 'Communicate as Backdoor User',
      'safe': true,
      'info': 'Attempts to create a new user, create HTTPS requests as that ' +
      'user and then deletes the user.'
    },
    {
      'type': 'string',
      'enum': ['ModifyShellStartupFiles'],
      'title': 'Modify Shell Startup Files',
      'safe': true,
      'info': 'Attempts to modify shell startup files, such as ~/.profile, ' +
      '~/.bashrc, ~/.bash_profile ' +
      'in linux, and profile.ps1 in Windows. Reverts modifications done' +
      ' afterwards.'
    },
    {
      'type': 'string',
      'enum': ['HiddenFiles'],
      'title': 'Hidden Files and Directories',
      'safe': true,
      'info': 'Attempts to create a hidden file and remove it afterwards.'
    },
    {
      'type': 'string',
      'enum': ['TrapCommand'],
      'title': 'Trap Command',
      'safe': true,
      'info': 'On Linux systems, attempts to trap a terminate signal in order ' +
      'to execute a command upon receiving that signal. Removes the trap afterwards.'
    },
    {
      'type': 'string',
      'enum': ['ChangeSetuidSetgid'],
      'title': 'Setuid and Setgid',
      'safe': true,
      'info': 'On Linux systems, attempts to set a new file's setuid and setgid bits.      'Removes the file afterwards.',
      'attack_techniques': ['T1166']
    },
    {
      'type': 'string',
      'enum': ['ScheduleJobs'],
      'title': 'Job Scheduling',
      'safe': true,
      'info': 'Attempts to create a scheduled job on the system and remove it.'
    },
    {
      'type': 'string',
      'enum': ['Timestomping'],
      'title': 'Timestomping',
      'safe': true,
      'info': 'Creates a temporary file and attempts to modify its time ' +
      'attributes. Removes the file afterwards.'
    },
    {
      'type': 'string',
      'enum': ['SignedScriptProxyExecution'],
      'title': 'Signed Script Proxy Execution',
      'safe': false,
      'info': 'On Windows systems, attempts to execute an arbitrary file ' +
      'with the help of a pre-existing signed script.'
    },
    {
      'type': 'string',
      'enum': ['AccountDiscovery'],
      'title': 'Account Discovery',
      'safe': true,
      'info': 'Attempts to get a listing of user accounts on the system.'
    },
    {
      'type': 'string',
      'enum': ['ClearCommandHistory'],
      'title': 'Clear Command History',
      'safe': false,
      'info': 'Attempts to clear the command history.'
    },
    {
      'type': 'string',
      'enum': ['ProcessListCollection'],
      'title': 'Process List Collector',
      'safe': true,
      'info': 'Collects a list of running processes on the machine.'
    }
  ]


}
export default POST_BREACH_ACTIONS;
