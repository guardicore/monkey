import PROPAGATION_CONFIGURATION_SCHEMA from './propagation/propagation.js';
import CREDENTIAL_COLLECTORS from './credentialCollectors.js';
import RANSOMWARE_SCHEMA from './ransomware';

export const SCHEMA = {
  'title': 'Monkey',
  'type': 'object',
  'properties': {
    'propagation': PROPAGATION_CONFIGURATION_SCHEMA,
    'payloads': RANSOMWARE_SCHEMA,
    'credential_collectors': {
      'title': 'Credential collectors',
      'type': 'array',
      'uniqueItems': true,
      'items': CREDENTIAL_COLLECTORS
    },
    'advanced': {
      'title': 'Advanced',
      'type': 'object',
      'properties':{
        'keep_tunnel_open_time': {
          'title': 'Keep tunnel open time',
          'type': 'integer',
          'default': 30,
          'minimum': 0,
          'description': 'Time in seconds after the last exploit for keeping the tunnel open'
        }
      }
    }
  },
  'options': {'collapsed': true}
}
