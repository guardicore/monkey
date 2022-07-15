import {defaultCredentials} from '../../services/configuration/propagation/credentials';
import _ from 'lodash';

export function reformatConfig(config, reverse = false) {
  if (reverse) {
    config['payloads'] = [{'name': 'ransomware', 'options': config['payloads']}]
  } else {
    config['payloads'] = config['payloads'][0]['options'];
  }
  return config;
}

export function formatCredentialsForForm(credentials) {
  console.log(credentials);
  let formattedCredentials = _.clone(defaultCredentials);
  for (let i = 0; i < credentials.length; i++) {
    for (let j = 0; j < credentials[i].identities.length; j++) {
      formattedCredentials['exploit_user_list'].push(credentials[i]['identities'][j].username)
    }
    for (let j = 0; j < credentials[i].secrets.length; j++) {
      console.log(credentials[i])
      let secret = credentials[i]['secrets'][j];
      if (secret['credential_type'] === 'PASSWORD') {
        formattedCredentials['exploit_password_list'].push(secret['password'])
      }
      if (secret['credential_type'] === 'NT_HASH') {
        formattedCredentials['exploit_ntlm_hash_list'].push(secret['nt_hash'])
      }
      if (secret['credential_type'] === 'LM_HASH') {
        formattedCredentials['exploit_lm_hash_list'].push(secret['lm_hash'])
      }
      if (secret['credential_type'] === 'SSH_KEY') {
        let keypair = {'public_key': secret['public_key'], 'private_key': secret['private_key']}
        formattedCredentials['exploit_ssh_keys'].push(keypair)
      }
    }
  }
  return formattedCredentials;
}

export function formatCredentialsForIsland(credentials) {
  let formattedCredentials = [];
  let usernames = credentials['exploit_user_list'];
  for (let i = 0; i < usernames.length; i++) {
    formattedCredentials.push({
      'identities': [{'username': usernames[i], 'credential_type': 'USERNAME'}],
      'secrets': []
    })
  }

  let passwords = credentials['exploit_password_list'];
  for (let i = 0; i < passwords.length; i++) {
    formattedCredentials.push({
      'identities': [],
      'secrets': [{'credential_type': 'PASSWORD', 'password': passwords[i]}]
    })
  }

  let nt_hashes = credentials['exploit_ntlm_hash_list'];
  for (let i = 0; i < nt_hashes.length; i++) {
    formattedCredentials.push({
      'identities': [],
      'secrets': [{'credential_type': 'NT_HASH', 'nt_hash': nt_hashes[i]}]
    })
  }

  let lm_hashes = credentials['exploit_lm_hash_list'];
  for (let i = 0; i < lm_hashes.length; i++) {
    formattedCredentials.push({
      'identities': [],
      'secrets': [{'credential_type': 'LM_HASH', 'lm_hash': lm_hashes[i]}]
    })
  }

  let ssh_keys = credentials['exploit_ssh_keys'];
  for (let i = 0; i < ssh_keys.length; i++) {
    formattedCredentials.push({
      'identities': [],
      'secrets': [{'credential_type': 'SSH_KEYPAIR', 'private_key': ssh_keys[i]['private_key'],
      'public_key': ssh_keys[i]['public_key']}]
    })
  }

  return formattedCredentials;
}
