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
