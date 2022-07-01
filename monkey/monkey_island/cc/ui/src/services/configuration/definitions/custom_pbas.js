export const customPBAConfigurationSchema = {
  'title': 'Custom PBA',
  'properties': {
    'linux_command': {
      'title': 'Linux post-breach command',
      'type': 'string',
      'default': '',
      'description': 'Command to be executed after breaching. ' +
      'Use this field to run custom commands or execute the uploaded ' +
      'file on exploited machines.\nExample: ' +
      '"chmod +x ./my_script.sh; ./my_script.sh ; rm ./my_script.sh"'
    },
    'linux_filename': {
      'title': 'Linux post-breach file',
      'type': 'string',
      'description': 'File to be uploaded after breaching. ' +
      'Use the "Linux post-breach command" field to ' +
      'change permissions, run, or delete the file. ' +
      'Reference your file by filename.'
    },
    'windows_command': {
      'title': 'Windows post-breach command',
      'type': 'string',
      'default': '',
      'description': 'Command to be executed after breaching. ' +
      'Use this field to run custom commands or execute the uploaded ' +
      'file on exploited machine.\nExample: ' +
      '"my_script.bat & del my_script.bat"'
    },
    'windows_filename':{
      'title': 'Windows post-breach file',
      'type': 'string',
      'description': 'File to be uploaded after breaching. ' +
      'Use the "Windows post-breach command" field to ' +
      'change permissions, run or delete the file. ' +
      'Reference your file by filename.'
    }
  }
}
