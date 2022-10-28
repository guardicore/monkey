import {CredentialTitle, SecretType} from '../utils/CredentialTitle.js';

export function getCredentialsUsernames(credentials): string[]{
  let usernames = [];
  for (let i = 0; i < credentials.length; i++) {
    let username = credentials[i]['identity'];
    if (username !== null) {
      usernames.push(username['username']);
    }
  }
  return usernames;
}

export type Secret = {
  title: CredentialTitle
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
  if (Object.prototype.hasOwnProperty.call(secret, SecretType.Password)) {
    return {'title': CredentialTitle.Password, 'content': secret[SecretType.Password]}
  }
  if (Object.prototype.hasOwnProperty.call(secret, SecretType.NTHash)) {
    return {'title': CredentialTitle.NTHash, 'content': secret[SecretType.NTHash]}
  }
  if (Object.prototype.hasOwnProperty.call(secret, SecretType.LMHash)) {
    return {'title': CredentialTitle.LMHash, 'content': secret[SecretType.LMHash]}
  }
  if (Object.prototype.hasOwnProperty.call(secret, SecretType.PrivateKey)) {
    return {
      'title': CredentialTitle.SSHKeys,
      'content': secret[SecretType.PrivateKey]
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
