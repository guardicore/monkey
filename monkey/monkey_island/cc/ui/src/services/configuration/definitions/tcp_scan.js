export const tcpScanConfigurationSchema = {
  'title': 'TCP scanner',
  'type': 'object',
  'properties': {
    'ports': {
      'title': 'TCP target ports',
      'type': 'array',
      'items': {
        'type': 'integer'
      },
      'default': [22,2222,445,135,389,80,8080,443,8008,3306,7001,8088,5885,5986],
      'description': 'List of TCP ports the monkey will check whether they\'re open'
    },
    'timeout': {
      'title': 'TCP scan timeout',
      'format': 'float',
      'type': 'number',
      'description': 'Maximum time to wait for TCP response.'
    }
  }
}
