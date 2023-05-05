const MASQUERADE = {
  'title': 'Masquerade',
  'type': 'object',
  'description': 'To identify malware in a file, one common approach is to search for specific ' +
  'strings or unique byte sequences.\nIn order to enhance Infection Monkey\'s malware emulation,'+
  'custom data can be injected into agent binaries, allowing the agents to imitate various types of malware. '+
  'This feature can be particularly helpful when testing custom detection rules.',
  'properties': {
    'linux_masque_strings': {
      'title': 'Linux Masque Strings',
      'type': 'array',
      'uniqueItems': true,
      'items': {'type': 'string'},
      'default': [],
      'description': 'List of masque strings that will be insert to the Linux Agent binaries '
    },
    'windows_masque_strings': {
      'title': 'Windows Masque Strings',
      'type': 'array',
      'uniqueItems': true,
      'items': {'type': 'string'},
      'default': [],
      'description': 'List of masque strings that will be insert to the Windows Agent binaries '
    }

  }
}

export const defaultMasques = {
 'linux_masque_strings': [],
 'windows_masque_strings': []
}

export default MASQUERADE;
