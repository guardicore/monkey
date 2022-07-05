import {icmpScanConfigurationSchema} from './icmp_scan.js';
import {scanTargetConfigurationSchema} from './scan_target.js';
import {tcpScanConfigurationSchema} from './tcp_scan.js';

export const networkScanConfigurationSchema  = {
  'title': 'Network analysis',
  'type': 'object',
  'properties': {
    'fingerprinters': {
      'title': 'Fingerprinters',
      'type': 'array',
      'uniqueItems': true,
      'items': {
        '$ref': '#/definitions/fingerprinter_classes'
      }
    },
    'icmp': icmpScanConfigurationSchema,
    'targets': scanTargetConfigurationSchema,
    'tcp': tcpScanConfigurationSchema
  }
}
