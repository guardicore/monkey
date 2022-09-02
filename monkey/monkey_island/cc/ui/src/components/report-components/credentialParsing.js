import {CredentialTypes, SecretTypes} from '../utils/CredentialTypes.js';

export function getAllUsernames(stolen, configured) {
  let usernames = new Set();
  usernames.add(...getCredentialsUsernames(stolen));
  usernames.add(...getCredentialsUsernames(configured));
  return Array.from(usernames);
}

export function getCredentialsUsernames(credentials) {
  let usernames = [];
  for (let i = 0; i < credentials.length; i++) {
    let username = credentials[i]['identity'];
    if (username !== null) {
      usernames.push(username['username']);
    }
  }
  return usernames;
}

export function getAllSecrets(stolen, configured) {
  let secrets = new Set();
  for (let i = 0; i < stolen.length; i++) {
    let secret = stolen[i]['secret'];
    if (secret !== null) {
      secrets.add(reformatSecret(secret));
    }
  }
  for (let i = 0; i < configured.length; i++) {
    let secret = configured[i]['secret'];
    if (secret !== null) {
      secrets.add(reformatSecret(secret));
    }
  }
  return Array.from(secrets);
}

function reformatSecret(secret) {
  if (secret.hasOwnProperty(SecretTypes.Password)) {
    return {'type': CredentialTypes.Password, 'content': secret[SecretTypes.Password]}
  }
  if (secret.hasOwnProperty(SecretTypes.NTHash)) {
    return {'type': CredentialTypes.NTHash, 'content': secret[SecretTypes.NTHash]}
  }
  if (secret.hasOwnProperty(SecretTypes.LMHash)) {
    return {'type': CredentialTypes.LMHash, 'content': secret[SecretTypes.LMHash]}
  }
  if (secret.hasOwnProperty(SecretTypes.PrivateKey)) {
    return {
      'type': CredentialTypes.SSHKeys,
      'content': secret[SecretTypes.PrivateKey]
    }
  }
}

export function getCredentialsTableData(credentials) {
  let table_data = [];

  let identites = getCredentialsUsernames(credentials);
  let secrets = getAllSecrets(credentials, [])

  for (let i = 0; i < credentials.length; i++) {
    let row_data = {};
    row_data['username'] = identites[i];
    row_data['type'] = secrets[i]['type'];
    table_data.push(row_data);
  }

  return table_data;
}
