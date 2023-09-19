import {
  IP,
  IP_RANGE,
  VALID_BASE64,
  VALID_EMAIL_ADDRESS
} from './ValidationFormats';


export default function transformErrors(errors) {
  return errors.map(error => {
    if (error.name === 'type') {
      error.message = `Field can't be empty.`;
    } else if (error.name === 'format' && error.params.format === IP_RANGE) {
      error.message = 'Invalid IP range, refer to description for valid examples.';
    } else if (error.name === 'format' && error.params.format === IP) {
      error.message = 'Invalid IP.';
    } else if (error.name === 'format' && error.params.format === VALID_BASE64) {
      error.message = 'Must be a Base64 value.';
    } else if (error.name === 'format' && error.params.format === VALID_EMAIL_ADDRESS) {
      error.message = 'Invalid email address.';
    }
    return error;
  });
}
