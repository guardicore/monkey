import PROPAGATION_CONFIGURATION_SCHEMA from './propagation/propagation.js';
import CREDENTIAL_COLLECTORS from './credentialCollectors.js';
import POST_BREACH_ACTIONS from './postBreachActions.js';
import RANSOMWARE_SCHEMA from './ransomware';
import CUSTOM_PBA_CONFIGURATION_SCHEMA from './customPBAs';

export const SCHEMA = {
  'title': 'Monkey',
  'type': 'object',
  'properties': {
    'propagation': PROPAGATION_CONFIGURATION_SCHEMA,
    'post_breach_actions': {
      'title': 'Post-breach actions',
      'type': 'array',
      'uniqueItems':  true,
      'items': POST_BREACH_ACTIONS
    },
    'custom_pbas': CUSTOM_PBA_CONFIGURATION_SCHEMA,
    'payloads': RANSOMWARE_SCHEMA,
    'credential_collectors': {
      'title': 'Credential collectors',
      'type': 'array',
      'uniqueItems': true,
      'items': CREDENTIAL_COLLECTORS,
      'default': [
        'MimikatzCollector',
        'SSHCollector'
      ]
    },
    'advanced': {
      'title': 'Advanced',
      'type': 'object',
      'properties':{
        'keep_tunnel_open_time': {
          'title': 'Keep tunnel open time',
          'format': 'float',
          'type': 'number',
          'default': 30,
          'description': 'Time to keep tunnel open before going down after last exploit (in seconds)'
        }
      }
    }
  },
  'options': {'collapsed': true}
}
