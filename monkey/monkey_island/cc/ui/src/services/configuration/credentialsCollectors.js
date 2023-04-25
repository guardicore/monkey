const CREDENTIALS_COLLECTORS = {
    'title': 'Credentials Collectors',
    'description': 'Click on a credentials collector for more information.',
    'type': 'object',
    'pluginDefs': {
      'MimikatzCollector':{'name': 'MimikatzCollector', 'options': {}},
      'SSHCollector':{'name': 'SSHCollector', 'options': {}}
    },
    'properties':{
      'name': {
        'type': 'string',
        'anyOf': [
          {
            'type': 'string',
            'enum': ['MimikatzCollector'],
            'title': 'Mimikatz Credentials Collector',
            'safe': true,
            'info': 'Collects credentials from Windows credential manager.'
          },
          {
            'type': 'string',
            'enum': ['SSHCollector'],
            'title': 'SSH Credentials Collector',
            'safe': true,
            'info': 'Searches users\' home directories and collects SSH keypairs.'
          }
        ]
      },
      'options': {
        'type': 'object'
      }
    }
}
export default CREDENTIALS_COLLECTORS
