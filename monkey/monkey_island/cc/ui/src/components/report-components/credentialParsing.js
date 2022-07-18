export function getAllUsernames(stolen, configured){
  let usernames = [];
  usernames.push(...getCredentialsUsernames(stolen));
  usernames.push(...getCredentialsUsernames(configured));
  return usernames;
}

export function getCredentialsUsernames(credentials) {
  let usernames = [];
  for(let i = 0; i < credentials.length; i++){
    usernames.push(credentials[i]['identity']['username']);
  }
  return usernames;
}

export function getAllSecrets(stolen, configured){
  let secrets = [];
  for(let i = 0; i < stolen.length; i++){
    secrets.push(getSecretsFromCredential(stolen[i]['secret']));
  }
  for(let i = 0; i < configured.length; i++){
    secrets.push(getSecretsFromCredential(configured[i]['secret']));
  }
  return secrets;
}

function getSecretsFromCredential(credential) {
  if(credential['credential_type'] === 'SSH_KEYPAIR'){
    return {'type': 'SSH keypair', 'content': credential['private_key']}
  }
  if(credential['credential_type'] === 'NT_HASH'){
    return {'type': 'NT hash', 'content': credential['nt_hash']}
  }
  if(credential['credential_type'] === 'LM_HASH'){
    return {'type': 'LM hash', 'content': credential['lm_hash']}
  }
  if(credential['credential_type'] === 'PASSWORD'){
    return {'type': 'Password', 'content': credential['password']}
  }
}

export function getCredentialsTableData(credentials) {

    let table_data = [];

    let identites = getCredentialsUsernames(credentials);
    let secrets = getAllSecrets(credentials, [])

    for(let i=0; i<credentials.length; i++) {
      let row_data = {};
      row_data['username'] = identites[i];
      row_data['type'] = secrets[i]['type'];
      table_data.push(row_data);
    }

    return table_data;
}
