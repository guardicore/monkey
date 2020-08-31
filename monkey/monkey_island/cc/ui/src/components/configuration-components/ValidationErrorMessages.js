import {IP, IP_RANGE} from './ValidationFormats';

export default function transformErrors(errors) {
  return errors.map(error => {
    if (error.name === 'type') {
      error.message = 'Field can\'t be empty.'
    } else if (error.name === 'format' && error.params.format === IP_RANGE) {
      error.message = 'Invalid IP range, refer to description for valid examples.'
    } else if (error.name === 'format' && error.params.format === IP) {
      error.message = 'Invalid IP.'
    }
    return error;
  });
}
