import {defaultCredentials} from '../../services/configuration/propagation/credentials';
import {PlaintextTypes, SecretTypes} from '../utils/CredentialTitles.js';
import _ from 'lodash';

export function reformatConfig(config, reverse = false) {
  let formattedConfig = _.clone(config);

  if (reverse) {
    if (formattedConfig['payloads'].length === 1) {
      // Second click on Export
      formattedConfig['payloads'] = [{
        'name': 'ransomware',
        'options': formattedConfig['payloads'][0]['options']
      }];
    } else {
      formattedConfig['payloads'] = [{
        'name': 'ransomware',
        'options': formattedConfig['payloads']
      }];
    }
    formattedConfig['keep_tunnel_open_time'] = formattedConfig['advanced']['keep_tunnel_open_time'];
  } else {
    if (formattedConfig['payloads'].length !== 0) {
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
  let formattedCredentials = _.cloneDeep(defaultCredentials);
  for (let i = 0; i < credentials.length; i++) {
    let identity = credentials[i]['identity'];
    if (identity !== null) {
      formattedCredentials['exploit_user_list'].push(identity.username)
    }

    let secret = credentials[i]['secret'];
    if (secret !== null) {
      if (Object.prototype.hasOwnProperty.call(secret, SecretTypes.Password)) {
        formattedCredentials['exploit_password_list'].push(secret[SecretTypes.Password])
      }
      if (Object.prototype.hasOwnProperty.call(secret, SecretTypes.NTHash)) {
        formattedCredentials['exploit_ntlm_hash_list'].push(secret[SecretTypes.NTHash])
      }
      if (Object.prototype.hasOwnProperty.call(secret, SecretTypes.LMHash)) {
        formattedCredentials['exploit_lm_hash_list'].push(secret[SecretTypes.LMHash])
      }
      if (Object.prototype.hasOwnProperty.call(secret, SecretTypes.PrivateKey)) {
        let keypair = {
          'public_key': secret[PlaintextTypes.PublicKey],
          'private_key': secret[SecretTypes.PrivateKey]
        }
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
      'identity': {'username': usernames[i]},
      'secret': null
    })
  }

  formattedCredentials.push(...getFormattedCredentials(credentials['exploit_password_list'], SecretTypes.Password))
  formattedCredentials.push(...getFormattedCredentials(credentials['exploit_ntlm_hash_list'], SecretTypes.NTHash))
  formattedCredentials.push(...getFormattedCredentials(credentials['exploit_lm_hash_list'], SecretTypes.LMHash))

  let ssh_keys = credentials['exploit_ssh_keys'];
  for (let i = 0; i < ssh_keys.length; i++) {
    formattedCredentials.push({
      'identity': null,
      'secret': {
        'private_key': ssh_keys[i]['private_key'],
        'public_key': ssh_keys[i]['public_key']
      }
    })
  }

  return formattedCredentials;
}

function getFormattedCredentials(credentials, keyOfSecret) {
  let formattedCredentials = [];
  for (let i = 0; i < credentials.length; i++) {
    formattedCredentials.push({
      'identity': null,
      'secret': {[keyOfSecret]: credentials[i]}
    })
  }
  return formattedCredentials;
}
