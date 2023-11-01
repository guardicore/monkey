import ICMP_SCAN_CONFIGURATION_SCHEMA from './icmpScan.js';
import SCAN_TARGET_CONFIGURATION_SCHEMA from './scanTarget.js';
import FINGERPRINTER_CLASSES from './fingerprinterClasses';
import TCP_SCAN_CONFIGURATION_SCHEMA from './tcpScan';

const NETWORK_SCAN_CONFIGURATION_SCHEMA  = {
  'title': 'Network analysis',
  'type': 'object',
  'properties': {
    'fingerprinters': {
      'title': 'Fingerprinters',
      'type': 'object',
      'uniqueItems': true,
      'items': FINGERPRINTER_CLASSES
    },
    'icmp': ICMP_SCAN_CONFIGURATION_SCHEMA,
    'targets': SCAN_TARGET_CONFIGURATION_SCHEMA,
    'tcp': TCP_SCAN_CONFIGURATION_SCHEMA
  }
}

export default NETWORK_SCAN_CONFIGURATION_SCHEMA;
