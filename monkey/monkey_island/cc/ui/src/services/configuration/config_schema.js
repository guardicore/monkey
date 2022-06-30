import {customPBAConfigurationSchema} from './definitions/custom_pbas.js';
import {pluginConfigurationSchema} from './definitions/plugins.js';
import {propagationConfigurationSchema} from './definitions/propagation.js';
import {bruteForceExploiters, vulnerabilityExploiters} from './definitions/exploiter_classes.js';

export const SCHEMA = {
  'title': 'Monkey',
  'type': 'object',
  'definitions': {
    'brute_force_classes': bruteForceExploiters,
    'vulnerability_classes': vulnerabilityExploiters
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
      'type': 'array',
      'items': pluginConfigurationSchema,
      'default': [
        {'name': 'MimikatzCollector', 'safe': true, 'options':{}},
        {'name': 'SSHCollector', 'safe': true, 'options':{}}
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
