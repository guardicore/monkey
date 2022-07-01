import {customPBAConfigurationSchema} from './definitions/custom_pbas.js';
import {pluginConfigurationSchema} from './definitions/plugins.js';
import {propagationConfigurationSchema} from './definitions/propagation.js';
import {bruteForceExploiters, vulnerabilityExploiters} from './definitions/exploiter_classes.js';
import {credentialCollectors} from './definitions/credential_collectors.js';

export const SCHEMA = {
  'title': 'Monkey',
  'type': 'object',
  'definitions': {
    'brute_force_classes': bruteForceExploiters,
    'vulnerability_classes': vulnerabilityExploiters,
    'credential_collectors_classes': credentialCollectors
  },
  'properties': {
    'propagation': propagationConfigurationSchema,
    'post_breach_actions': {
      'title': 'Post-breach actions',
      'type': 'object',
      'properties': {
        'pba_list': {
          'title': 'PBAs',
          'type': 'array',
          'items': pluginConfigurationSchema,
          'default': [
            {'name': 'CommunicateAsBackdoorUser','safe': true, 'options': {}},
            {'name': 'ModifyShellStartupFiles', 'safe': true, 'options': {}}
          ]
        },
        'custom_pbas': customPBAConfigurationSchema
      }
    },
    'payloads': {
      'title': 'Payloads',
      'type': 'array',
      'items': pluginConfigurationSchema,
      'default': [
        {'name': 'ransomware', 'safe': true, 'options': {}}
      ]
    },
    'credential_collectors': {
      'title': 'Credential collectors',
      'properties': {
        'collectors': {
          'title': 'Credential collectors',
          'type': 'array',
          'uniqueItems': true,
          'items': {
            '$ref': '#/definitions/credential_collectors_classes'
          },
          'default': [
            'MimikatzCollector',
            'SSHCollector'
          ]
        }
      }
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
