const MASQUERADE = {
  'title': 'Masquerade',
  'type': 'object',
  'description': 'Infection Monkey can emulate malware by injecting custom data into Agent binaries.\n'+
    'This feature can be particularly helpful when testing custom detection rules.',
  'properties': {
    'linux_masque_strings': {
      'title': 'Linux Masque Strings',
      'type': 'array',
      'uniqueItems': true,
      'items': {'type': 'string'},
      'default': [],
      'description': 'List of masque strings that will be applied to the Linux Agent binary.'
    },
    'windows_masque_strings': {
      'title': 'Windows Masque Strings',
      'type': 'array',
      'uniqueItems': true,
      'items': {'type': 'string'},
      'default': [],
      'description': 'List of masque strings that will be applied to the Windows Agent binary.'
    }

  }
}

export const defaultMasques = {
 'linux_masque_strings': [],
 'windows_masque_strings': []
}

export default MASQUERADE;
