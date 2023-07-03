export enum CredentialTitle {
  Password = 'Clear Password',
  SSHKeys = 'Clear SSH private key',
  LMHash = 'LM hash',
  NTHash = 'NT hash',
  Username = 'Username'
}

export enum IdentityType {
  Username = 'username',
  EmailAddress = 'email_address'
}

export enum SecretType {
  Password = 'password',
  PrivateKey = 'private_key',
  LMHash = 'lm_hash',
  NTHash = 'nt_hash'
}

export enum PlaintextType {
  PublicKey = 'public_key'
}

export const SECRET_TYPES = {
    password: 'password',
    lm: 'lm_hash',
    ntlm: 'nt_hash',
    ssh_public_key: 'public_key',
    ssh_private_key: 'private_key'
}
