import { CredentialTitle, SecretType } from "../utils/CredentialTitle";
import _ from "lodash";

export function getAllUsernames(stolen, configured): string[] {
  let usernames = new Set([
    ...getCredentialsUsernames(stolen),
    ...getCredentialsUsernames(configured),
  ]);
  return Array.from(usernames);
}

export function getCredentialsUsernames(credentials): string[] {
  let usernames = [];
  for (let credential of credentials) {
    let identity = credential["identity"];
    if (identity !== null && identity !== undefined) {
      if ("username" in identity) {
        usernames.push(identity["username"]);
      }
    }
  }
  return usernames;
}

export type Secret = {
  title: CredentialTitle;
  content: string;
};

export function getAllSecrets(stolen, configured = []) {
  let secrets = [];
  let stolenSecrets = stolen
    .map((cred) => cred["secret"])
    .filter((cred) => cred !== null);
  let configuredSecrets = configured
    .map((cred) => cred["secret"])
    .filter((cred) => cred !== null);
  let allSecrets = [...stolenSecrets, ...configuredSecrets];

  for (let secret of allSecrets) {
    let formatted_secret = reformatSecret(secret);
    if (!_.find(secrets, formatted_secret)) {
      secrets.push(formatted_secret);
    }
  }
  return secrets;
}

export function reformatSecret(secret): Secret {
  if (Object.prototype.hasOwnProperty.call(secret, SecretType.Password)) {
    return {
      title: CredentialTitle.Password,
      content: secret[SecretType.Password],
    };
  }
  if (Object.prototype.hasOwnProperty.call(secret, SecretType.NTHash)) {
    return {
      title: CredentialTitle.NTHash,
      content: secret[SecretType.NTHash],
    };
  }
  if (Object.prototype.hasOwnProperty.call(secret, SecretType.LMHash)) {
    return {
      title: CredentialTitle.LMHash,
      content: secret[SecretType.LMHash],
    };
  }
  if (Object.prototype.hasOwnProperty.call(secret, SecretType.PrivateKey)) {
    return {
      title: CredentialTitle.SSHKeys,
      content: secret[SecretType.PrivateKey],
    };
  }
}
