const MASQUERADE = {
  'title': 'Masquerade',
  'type': 'object',
  'description': 'Infection Monkey can emulate malware by injecting custom data into Agent binaries.\n'+
    'This feature can be particularly helpful when testing custom detection rules.',
  'properties': {
    'linux_masque_string': {
      'title': 'Linux Masque',
      'type': 'string',
      'default': '',
      'description': 'A masque string that will be applied to the Linux Agent binary.'
    },
    'windows_masque_string': {
      'title': 'Windows Masque',
      'type': 'string',
      'default': '',
      'description': 'A masque string that will be applied to the Windows Agent binary.'
    }

  }
}

export const defaultMasques = {
 'linux_masque_string': [],
 'windows_masque_string': []
}

export default MASQUERADE;
