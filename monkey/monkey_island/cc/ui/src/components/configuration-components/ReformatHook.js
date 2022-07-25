import {defaultCredentials} from '../../services/configuration/propagation/credentials';
import _ from 'lodash';

export function reformatConfig(config, reverse = false) {
  let formattedConfig = _.clone(config);

  if (reverse) {
    if(formattedConfig['payloads'].length === 1){
      // Second click on Export
      formattedConfig['payloads'] = [{'name': 'ransomware', 'options': formattedConfig['payloads'][0]['options']}];
    } else {
      formattedConfig['payloads'] = [{'name': 'ransomware', 'options': formattedConfig['payloads']}];
    }
    formattedConfig['keep_tunnel_open_time'] = formattedConfig['advanced']['keep_tunnel_open_time'];
  } else {
    if(formattedConfig['payloads'].length !== 0)
    {
      formattedConfig['payloads'] = formattedConfig['payloads'][0]['options'];
    } else {
      formattedConfig['payloads'] = {'encryption': {}, 'other_behaviors': {}}
    }
    formattedConfig['advanced'] = {};
    formattedConfig['advanced']['keep_tunnel_open_time'] = formattedConfig['keep_tunnel_open_time'];
  }
  return formattedConfig;
}

export function formatCredentialsForForm(credentials) {
  let formattedCredentials = _.clone(defaultCredentials);
  for (let i = 0; i < credentials.length; i++) {
    let identity = credentials[i]['identity'];
    if(identity !== null) {
      formattedCredentials['exploit_user_list'].push(identity.username)
    }

    let secret = credentials[i]['secret'];
    if(secret !== null){
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

  formattedCredentials['exploit_user_list'] = [...new Set(formattedCredentials['exploit_user_list'])];
  formattedCredentials['exploit_password_list'] = [...new Set(formattedCredentials['exploit_password_list'])];
  formattedCredentials['exploit_ntlm_hash_list'] = [...new Set(formattedCredentials['exploit_ntlm_hash_list'])];
  formattedCredentials['exploit_lm_hash_list'] = [...new Set(formattedCredentials['exploit_lm_hash_list'])];

  return formattedCredentials;
}

export function formatCredentialsForIsland(credentials) {
  let formattedCredentials = [];
  let usernames = credentials['exploit_user_list'];
  for (let i = 0; i < usernames.length; i++) {
    formattedCredentials.push({
      'identity': {'username': usernames[i], 'credential_type': 'USERNAME'},
      'secret': null
    })
  }

  let passwords = credentials['exploit_password_list'];
  for (let i = 0; i < passwords.length; i++) {
    formattedCredentials.push({
      'identity': null,
      'secret': {'credential_type': 'PASSWORD', 'password': passwords[i]}
    })
  }

  let nt_hashes = credentials['exploit_ntlm_hash_list'];
  for (let i = 0; i < nt_hashes.length; i++) {
    formattedCredentials.push({
      'identity': null,
      'secret': {'credential_type': 'NT_HASH', 'nt_hash': nt_hashes[i]}
    })
  }

  let lm_hashes = credentials['exploit_lm_hash_list'];
  for (let i = 0; i < lm_hashes.length; i++) {
    formattedCredentials.push({
      'identity': null,
      'secret': {'credential_type': 'LM_HASH', 'lm_hash': lm_hashes[i]}
    })
  }

  let ssh_keys = credentials['exploit_ssh_keys'];
  for (let i = 0; i < ssh_keys.length; i++) {
    formattedCredentials.push({
      'identity': null,
      'secret': {'credential_type': 'SSH_KEYPAIR', 'private_key': ssh_keys[i]['private_key'],
      'public_key': ssh_keys[i]['public_key']}
    })
  }

  return formattedCredentials;
}
