import { IP, IP_RANGE, VALID_FILE_EXTENSION, VALID_RANSOMWARE_TARGET_PATH_LINUX, VALID_RANSOMWARE_TARGET_PATH_WINDOWS } from './ValidationFormats';

let invalidDirMessage = 'Invalid directory. Path should be absolute or begin with an environment variable.';

export default function transformErrors(errors) {
  return errors.map(error => {
    if (error.name === 'type') {
      error.message = 'Field can\'t be empty.'
    } else if (error.name === 'format' && error.params.format === IP_RANGE) {
      error.message = 'Invalid IP range, refer to description for valid examples.'
    } else if (error.name === 'format' && error.params.format === IP) {
      error.message = 'Invalid IP.'
    } else if (error.name === 'format' && error.params.format === VALID_FILE_EXTENSION) {
      error.message = 'Invalid file extension.'
    } else if (error.name === 'format' && error.params.format === VALID_RANSOMWARE_TARGET_PATH_LINUX) {
      error.message = invalidDirMessage
    } else if (error.name === 'format' && error.params.format === VALID_RANSOMWARE_TARGET_PATH_WINDOWS) {
      error.message = invalidDirMessage
    }
    return error;
  });
}
