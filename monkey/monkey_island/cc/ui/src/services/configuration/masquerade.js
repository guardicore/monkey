const MASQUERADE = {
  'title': 'Masquerade',
  'type': 'object',
  'properties': {
    'masque_list': {
      'title': 'Masque list',
      'type': 'array',
      'uniqueItems': true,
      'items': {'type': 'string'},
      'default': [],
      'description': 'List of masque strings that will be appended to the agent binaries '
    }
  }
}

export const defaultMasques = {
 'masque_list': []
}

export default MASQUERADE;
