import {CredentialTitles, SecretTypes} from '../utils/CredentialTitles.js';

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
  if (Object.prototype.hasOwnProperty.call(secret, SecretTypes.Password)) {
    return {'title': CredentialTitles.Password, 'content': secret[SecretTypes.Password]}
  }
  if (Object.prototype.hasOwnProperty.call(secret, SecretTypes.NTHash)) {
    return {'title': CredentialTitles.NTHash, 'content': secret[SecretTypes.NTHash]}
  }
  if (Object.prototype.hasOwnProperty.call(secret, SecretTypes.LMHash)) {
    return {'title': CredentialTitles.LMHash, 'content': secret[SecretTypes.LMHash]}
  }
  if (Object.prototype.hasOwnProperty.call(secret, SecretTypes.PrivateKey)) {
    return {
      'title': CredentialTitles.SSHKeys,
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
    row_data['title'] = secrets[i]['title'];
    table_data.push(row_data);
  }

  return table_data;
}
