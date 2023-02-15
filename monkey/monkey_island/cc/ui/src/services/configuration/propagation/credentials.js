const CREDENTIALS = {
  'title': 'Credentials',
  'type': 'object',
  'properties': {
    'exploit_user_list': {
      'title': 'Exploit user list',
      'type': 'array',
      'uniqueItems': true,
      'items': {'type': 'string'},
      'default': [],
      'description': 'List of usernames that will be used by exploiters that need ' +
        'credentials, like SSH brute-forcing.'
    },
    'exploit_password_list': {
      'title': 'Exploit password list',
      'type': 'array',
      'uniqueItems': true,
      'items': {'type': 'string'},
      'default': [],
      'description': 'List of passwords that will be used by exploiters that need ' +
        'credentials, like SSH brute-forcing.'
    },
    'exploit_lm_hash_list': {
      'title': 'Exploit LM hash list',
      'type': 'array',
      'uniqueItems': true,
      'items': {'type': 'string'},
      'default': [],
      'description': 'List of LM hashes to use on exploits using credentials'
    },
    'exploit_ntlm_hash_list': {
      'title': 'Exploit NTLM hash list',
      'type': 'array',
      'uniqueItems': true,
      'items': {'type': 'string'},
      'default': [],
      'description': 'List of NTLM hashes to use on exploits using credentials'
    },
    'exploit_ssh_keys': {
      'title': 'SSH key pairs list',
      'type': 'array',
      'uniqueItems': true,
      'default': [],
      'items': {
        'type': 'object',
        'title': 'SSH keypair',
        'properties': {
          'public_key': {
            'title': 'Public Key',
            'type': 'string'
          },
          'private_key': {
            'title': 'Private Key',
            'type': 'string'
          }
        }
      },
      'description': 'List of SSH key pairs to use, when trying to ssh into servers'
    }
  }
}

export const defaultCredentials = {
 'exploit_user_list': [],
 'exploit_password_list': [],
 'exploit_lm_hash_list': [],
 'exploit_ntlm_hash_list': [],
 'exploit_ssh_keys': []
}

export default CREDENTIALS;
