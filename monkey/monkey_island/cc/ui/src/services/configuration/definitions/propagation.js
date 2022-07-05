import {exploitationConfigurationSchema} from './exploitation.js';
import {networkScanConfigurationSchema} from './network_scan.js';

export const propagationConfigurationSchema = {
  'title': 'Propagation',
  'type': 'object',
  'properties': {
    'exploitation': exploitationConfigurationSchema,
    'maximum_depth': {
      'title': 'Maximum scan depth',
      'type': 'integer',
      'minimum': 1,
      'default': 2,
      'description': 'Amount of hops allowed for the monkey to spread from the ' +
      'Island server. \n' +
      ' \u26A0' +
      ' Note that setting this value too high may result in the ' +
      'Monkey propagating too far, '+
      'if the "Local network scan" is enabled'
    },
    'network_scan': networkScanConfigurationSchema
  }
}
