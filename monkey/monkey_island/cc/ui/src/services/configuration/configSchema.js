import PROPAGATION_CONFIGURATION_SCHEMA from './propagation/propagation.js';
import CREDENTIALS_COLLECTORS from './credentialsCollectors.js';
import PAYLOADS from './payloads.js';
import POLYMORPHISM_SCHEMA from './polymorphism.js'
import {MASQUERADE} from './masquerade.js';

export const SCHEMA = {
  'title': 'Monkey',
  'type': 'object',
  'properties': {
    'propagation': PROPAGATION_CONFIGURATION_SCHEMA,
    'payloads': {
      'title': 'Payloads',
      'type': 'array',
      'uniqueItems': true,
      'items': PAYLOADS
    },
    'credentials_collectors': {
      'title': 'Credentials collectors',
      'type': 'array',
      'uniqueItems': true,
      'items': CREDENTIALS_COLLECTORS
    },
    'masquerade': MASQUERADE,
    'polymorphism': POLYMORPHISM_SCHEMA,
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
