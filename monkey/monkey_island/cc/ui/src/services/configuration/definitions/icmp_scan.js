export const icmpScanConfigurationSchema = {
  'title': 'Ping scanner',
  'type': 'object',
  'properties': {
    'timeout': {
      'format': 'float',
      'title': 'Ping scan timeout',
      'type': 'number',
      'description': 'Maximum time to wait for ping response'
    }
  }
}
