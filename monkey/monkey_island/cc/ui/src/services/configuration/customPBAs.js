const CUSTOM_PBA_CONFIGURATION_SCHEMA = {
  'title': 'Custom PBA',
  'properties': {
    'linux_command': {
      'title': 'Linux post-breach command',
      'type': 'string',
      'default': '',
      'description': 'The command executed after breaching. ' +
      'Use this field to run custom commands or execute the uploaded ' +
      'file on an exploited machine.\nExample: ' +
      '"chmod +x ./my_script.sh; ./my_script.sh ; rm ./my_script.sh"'
    },
    'linux_file': {
      'title': 'Linux post-breach file',
      'type': 'string',
      'format': 'data-url',
      'description': 'The file uploaded after breaching.' +
      'Use the "Linux post-breach command" field to ' +
      'change permissions, run or delete the file. ' +
      'Reference your file by filename.'
    },
    'linux_filename': {
      'title': 'Linux PBA filename',
      'type': 'string',
      'default': ''
    },
    'windows_command': {
      'title': 'Windows post-breach command',
      'type': 'string',
      'default': '',
      'description': 'The command executed after breaching.' +
      'Use this field to run custom commands or execute the uploaded ' +
      'file on an exploited machine.\nExample: ' +
      '"my_script.bat & del my_script.bat"'
    },
    'windows_file':{
      'title': 'Windows post-breach file',
      'type': 'string',
      'format': 'data-url',
      'description': 'The file uploaded after breaching. ' +
      'Use the "Windows post-breach command" field to ' +
      'change permissions, run or delete the file. ' +
      'Reference your file by filename.'
    },
    'windows_filename': {
      'title': 'Windows PBA filename',
      'type': 'string',
      'default': ''
    }
  }
}
export default CUSTOM_PBA_CONFIGURATION_SCHEMA;
