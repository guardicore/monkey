const ipRegex = '((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
const cidrNotationRegex = '([0-9]|1[0-9]|2[0-9]|3[0-2])'
const hostnameRegex = '^([A-Za-z0-9]*[A-Za-z]+[A-Za-z0-9]*.?)*([A-Za-z0-9]*[A-Za-z]+[A-Za-z0-9]*)$'

import * as emailValidator from 'email-validator';

export const IP_RANGE = 'ip-range';
export const IP = 'ip';
export const VALID_BASE64 = 'valid-base64';
export const VALID_EMAIL_ADDRESS = 'valid-email-address';


export const formValidationFormats = {
  [IP_RANGE]: buildIpRangeRegex(),
  [IP]: buildIpRegex(),
  [VALID_BASE64]: isBase64,
  [VALID_EMAIL_ADDRESS]: emailValidator.validate
};

var base64 = require('base64-js');

function isBase64(str) {
  try {
    base64.toByteArray(str);
    return true;
  } catch (error) {
    return false;
  }
}

function buildIpRangeRegex() {
  return new RegExp([
    '^' + ipRegex + '$|', // Single: IP
    '^' + ipRegex + '-' + ipRegex + '$|', // IP range: IP-IP
    '^' + ipRegex + '/' + cidrNotationRegex + '$|', // IP range with cidr notation: IP/cidr
    hostnameRegex // Hostname: target.tg
  ].join(''))
}

function buildIpRegex() {
  return new RegExp('^' + ipRegex + '$')
}
