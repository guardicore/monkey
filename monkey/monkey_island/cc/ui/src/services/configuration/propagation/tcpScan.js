const TCP_SCAN_CONFIGURATION_SCHEMA = {
  'title': 'TCP scanner',
  'type': 'object',
  'properties': {
    'ports': {
      'title': 'TCP target ports',
      'type': 'array',
      'items': {
        'type': 'integer',
        'minimum': 0,
        'maximum': 65535
      },
      'default': [22,2222,445,135,389,80,8080,443,8008,3306,7001,8088,5885,5986],
      'description': 'List of TCP ports the monkey will check whether they\'re open'
    },
    'timeout': {
      'title': 'TCP scan timeout',
      'type': 'number',
      'minimum': 0,
      'default': 1,
      'description': 'Maximum time to wait for TCP response in seconds'
    }
  }
}
export default TCP_SCAN_CONFIGURATION_SCHEMA;
