import CREDENTIALS from '../../services/configuration/propagation/credentials';
import {MASQUERADE} from '../../services/configuration/masquerade';
import {
  IdentityType,
  SECRET_TYPES
} from '../utils/CredentialTitle.tsx';
import _ from 'lodash';
import {CREDENTIALS_ROW_KEYS, isAllValuesInRowAreEmpty} from '../ui-components/credential-pairs/credentialPairsHelper';
import {nanoid} from 'nanoid';
import {reverseObject} from '../../utils/objectUtils';

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

export function formatCredentialsForForm(credentialsData = []) {
  const rows = [];
  const REVERSED_SECRET_TYPES = reverseObject(SECRET_TYPES)

  for (const item of credentialsData) {
    const { identity, secret } = item;
    const identityKey = identity?.[IdentityType.Username] || identity?.[IdentityType.EmailAddress];
    let existingRows = rows.filter(row => row.identity === identityKey);

    let canMutateExistingRow = false;

    for (const existingRow of existingRows) {
      let canMutate = true;

      if(!secret) break;
      for (const [key, value] of Object.entries(secret)) {
        const secretKey = REVERSED_SECRET_TYPES[key];

        if (secretKey && !existingRow[secretKey] && value) {
          existingRow[secretKey] = value;
        } else if (existingRow[secretKey] !== value) {
          canMutate = false;
          break;
        }
      }

      if (canMutate) {
        canMutateExistingRow = true;
        break;
      }
    }

    if (!canMutateExistingRow) {
      const newRow = {
        id: nanoid(),
        identity: identityKey,
        password: secret?.password || '',
        lm: secret?.lm_hash || '',
        ntlm: secret?.nt_hash || '',
        ssh_public_key: secret?.public_key || '',
        ssh_private_key: secret?.private_key || '',
        isNew: false
      };
      rows.push(newRow);
    }
  }

  return rows;
}

export function formatCredentialsForIsland(credentialsData) {
  let formattedCredentials = [];
  let identitiesWithEmptySecret = [];

  credentialsData.forEach(row => {
    let keysToIgnore = ['identity', 'ssh_private_key', 'ssh_public_key'];
    const identityValue = row?.identity || null;
    const identityType = identityValue ? (isEmail(row.identity) ? IdentityType.EmailAddress : IdentityType.Username) : null;
    const identityObj = identityType ? {[identityType]: identityValue} : null;
    const secretValue = {
      [SECRET_TYPES.ssh_private_key]: row?.ssh_private_key || null,
      [SECRET_TYPES.ssh_public_key]: row?.ssh_public_key || null
    };

    if(identityObj && !identitiesWithEmptySecret.includes(identityValue) && isAllValuesInRowAreEmpty(row, ['identity'])) {
      formattedCredentials.push(getCredentialPair(identityObj, null));
      identitiesWithEmptySecret.push(identityValue);
    } else {
      if (secretValue[SECRET_TYPES.ssh_private_key] || secretValue[SECRET_TYPES.ssh_public_key]) {
        formattedCredentials.push(getCredentialPair(identityObj, secretValue));
      }

      CREDENTIALS_ROW_KEYS.filter(key => !keysToIgnore.includes(key)).forEach(key => {
        const currentSecretObj = row[key] ? {[SECRET_TYPES[key]]: row[key]} : null;
        if (currentSecretObj) {
          formattedCredentials.push(getCredentialPair(identityObj, currentSecretObj));
        }
      });
    }
  });

  return formattedCredentials;
}

const getCredentialPair = (identity, secret) => {
  return {
    'identity': identity,
    'secret': secret
  }
}

function isEmail(str) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(str);
}
