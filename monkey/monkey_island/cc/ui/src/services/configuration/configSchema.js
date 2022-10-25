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
          'type': 'number',
          'default': 30,
          'description': 'Time to keep tunnel open before going down after last exploit (in seconds)'
        }
      }
    }
  },
  'options': {'collapsed': true}
}
