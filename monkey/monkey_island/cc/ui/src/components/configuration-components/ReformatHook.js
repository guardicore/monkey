import CREDENTIALS, {defaultCredentials} from '../../services/configuration/propagation/credentials';
import {MASQUERADE} from '../../services/configuration/masquerade';
import {IdentityType, PlaintextType, SecretType} from '../utils/CredentialTitle.tsx';
import _ from 'lodash';

export function reformatConfig(config, reverse = false) {
  let formattedConfig = _.cloneDeep(config);

  if (reverse) {
    formattedConfig['keep_tunnel_open_time'] = formattedConfig['advanced']['keep_tunnel_open_time'];
    delete formattedConfig['advanced'];

    formattedConfig['propagation']['maximum_depth'] = formattedConfig['propagation']['general']['maximum_depth'];
    delete formattedConfig['propagation']['general'];
  } else {
    formattedConfig['advanced'] = {};
    formattedConfig['advanced']['keep_tunnel_open_time'] = formattedConfig['keep_tunnel_open_time'];
    delete formattedConfig['keep_tunnel_open_time'];

    formattedConfig['propagation']['general'] = {};
    formattedConfig['propagation']['general']['maximum_depth'] = formattedConfig['propagation']['maximum_depth'];
    delete formattedConfig['propagation']['maximum_depth'];
  }

  return formattedConfig;
}

export function reformatSchema(schema) {
  schema['properties']['propagation']['properties']['credentials'] = CREDENTIALS;
  schema['properties']['masquerade'] = MASQUERADE;
  schema['properties']['propagation']['properties']['general'] = {
    'title': 'General',
    'type': 'object',
    'properties': {'maximum_depth': schema['properties']['propagation']['properties']['maximum_depth']}
  };
  delete schema['properties']['propagation']['properties']['maximum_depth'];
  schema['properties']['advanced'] = {
    'title': 'Advanced',
    'type': 'object',
    'properties': {
      'keep_tunnel_open_time': schema['properties']['keep_tunnel_open_time']
    }
  };
  delete schema['properties']['keep_tunnel_open_time'];
  return schema;
}

export function formatCredentialsForForm(credentials) {
  let formattedCredentials = _.cloneDeep(defaultCredentials);

  for (let i = 0; i < credentials.length; i++) {

    let identity = credentials[i]['identity'];
    if (identity !== null) {
      if (Object.prototype.hasOwnProperty.call(identity, IdentityType.Username)) {
        formattedCredentials['exploit_user_list'].push(identity[IdentityType.Username])
      }
      if (Object.prototype.hasOwnProperty.call(identity, IdentityType.EmailAddress)) {
        formattedCredentials['exploit_email_list'].push(identity[IdentityType.EmailAddress])
      }
    }

    let secret = credentials[i]['secret'];
    if (secret !== null) {
      if (Object.prototype.hasOwnProperty.call(secret, SecretType.Password)) {
        formattedCredentials['exploit_password_list'].push(secret[SecretType.Password])
      }
      if (Object.prototype.hasOwnProperty.call(secret, SecretType.NTHash)) {
        formattedCredentials['exploit_ntlm_hash_list'].push(secret[SecretType.NTHash])
      }
      if (Object.prototype.hasOwnProperty.call(secret, SecretType.LMHash)) {
        formattedCredentials['exploit_lm_hash_list'].push(secret[SecretType.LMHash])
      }
      if (Object.prototype.hasOwnProperty.call(secret, SecretType.PrivateKey)) {
        let keypair = {
          'private_key': secret[SecretType.PrivateKey]
        }
        if(secret[PlaintextType.PublicKey] !== null){
          keypair['public_key'] = secret[PlaintextType.PublicKey];
        }
        formattedCredentials['exploit_ssh_keys'].push(keypair)
      }
    }
  }

  formattedCredentials['exploit_user_list'] = [...new Set(formattedCredentials['exploit_user_list'])];
  formattedCredentials['exploit_email_list'] = [...new Set(formattedCredentials['exploit_email_list'])];
  formattedCredentials['exploit_password_list'] = [...new Set(formattedCredentials['exploit_password_list'])];
  formattedCredentials['exploit_ntlm_hash_list'] = [...new Set(formattedCredentials['exploit_ntlm_hash_list'])];
  formattedCredentials['exploit_lm_hash_list'] = [...new Set(formattedCredentials['exploit_lm_hash_list'])];

  return formattedCredentials;
}

export function formatCredentialsForIsland(credentials) {
  let formattedCredentials = [];

  formattedCredentials.push(...getFormattedIdentities(credentials['exploit_user_list'], IdentityType.Username))
  formattedCredentials.push(...getFormattedIdentities(credentials['exploit_email_list'], IdentityType.EmailAddress))

  formattedCredentials.push(...getFormattedSecrets(credentials['exploit_password_list'], SecretType.Password))
  formattedCredentials.push(...getFormattedSecrets(credentials['exploit_ntlm_hash_list'], SecretType.NTHash))
  formattedCredentials.push(...getFormattedSecrets(credentials['exploit_lm_hash_list'], SecretType.LMHash))

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

function getFormattedIdentities(credentials, keyOfIdentity) {
  let formattedCredentials = [];
  for (let i = 0; i < credentials.length; i++) {
    formattedCredentials.push({
      'identity': {[keyOfIdentity]: credentials[i]},
      'secret': null
    })
  }
  return formattedCredentials;
}

function getFormattedSecrets(credentials, keyOfSecret) {
  let formattedCredentials = [];
  for (let i = 0; i < credentials.length; i++) {
    formattedCredentials.push({
      'identity': null,
      'secret': {[keyOfSecret]: credentials[i]}
    })
  }
  return formattedCredentials;
}
