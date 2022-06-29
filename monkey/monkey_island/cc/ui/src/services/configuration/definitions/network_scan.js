import {pluginConfigurationSchema} from './plugins.js';
import {icmpScanConfigurationSchema} from './icmp_scan.js';
import {scanTargetConfigurationSchema} from './scan_target.js';
import {tcpScanConfigurationSchema} from './tcp_scan.js';

export const networkScanConfigurationSchema  = {
  'type': 'object',
  'additionalProperties': false,
  'properties': {
    'fingerprinters': {
      'title': 'Fingerprinters',
      'type': 'array',
      'items': pluginConfigurationSchema,
      'default': [
        {'name': 'SMBFinger', 'safe': true, 'options': {}},
        {'name': 'SSHFinger', 'safe': true, 'options': {}},
        {'name': 'HTTPFinger', 'safe': true, 'options': {}},
        {'name': 'MSSQLFinger', 'safe': true, 'options': {}},
        {'name': 'ElasticFinger', 'safe': true, 'options': {}}
      ]
    },
    'icmp': icmpScanConfigurationSchema,
    'targets': scanTargetConfigurationSchema,
    'tcp': tcpScanConfigurationSchema
  }
}
