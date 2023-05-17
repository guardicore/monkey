const ipRegex = '((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
const cidrNotationRegex = '([0-9]|1[0-9]|2[0-9]|3[0-2])'
const hostnameRegex = '^([A-Za-z0-9]*[A-Za-z]+[A-Za-z0-9]*.?)*([A-Za-z0-9]*[A-Za-z]+[A-Za-z0-9]*)$'

const fileExtensionRegex = /^(\.[A-Za-z0-9_]+)*$/

const linuxAbsolutePathRegex = /^\// // path starts with `/`
const linuxPathStartsWithEnvVariableRegex = /^\$/ // path starts with `$`
const linuxPathStartsWithTildeRegex = /^~/ // path starts with `~`

const windowsAbsolutePathRegex = /^([A-Za-z]:(\\|\/))/ // path starts like `C:\` OR `C:/`
const windowsEnvVarNonNumeric = '[A-Za-z#\\$\'\\(\\)\\*\\+,\\-\\.\\?@\\[\\]_`\\{\\}~ ]'
const windowsPathStartsWithEnvVariableRegex = new RegExp(
  `^%(${windowsEnvVarNonNumeric}+(${windowsEnvVarNonNumeric}|\\d)*)%`
) // path starts like `$` OR `%abc%`
const windowsUncPathRegex = /^\\{2}/ // Path starts like `\\`

const emptyRegex = /^$/

const emailAddressRegex = new RegExp(/^[\w\-.]+@([\w-]+\.)+[\w-]{2,4}$/)


export const IP_RANGE = 'ip-range';
export const IP = 'ip';
export const VALID_FILE_EXTENSION = 'valid-file-extension';
export const VALID_RANSOMWARE_TARGET_PATH_LINUX = 'valid-ransomware-target-path-linux';
export const VALID_RANSOMWARE_TARGET_PATH_WINDOWS = 'valid-ransomware-target-path-windows';
export const VALID_BASE64 = 'valid-base64';
export const VALID_EMAIL_ADDRESS = 'valid-email-address';


export const formValidationFormats = {
  [IP_RANGE]: buildIpRangeRegex(),
  [IP]: buildIpRegex(),
  [VALID_FILE_EXTENSION]: fileExtensionRegex,
  [VALID_RANSOMWARE_TARGET_PATH_LINUX]: buildValidRansomwarePathLinuxRegex(),
  [VALID_RANSOMWARE_TARGET_PATH_WINDOWS]: buildValidRansomwarePathWindowsRegex(),
  [VALID_BASE64]: isBase64,
  [VALID_EMAIL_ADDRESS]: emailAddressRegex
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

function buildValidRansomwarePathLinuxRegex() {
  return new RegExp([
    emptyRegex.source,
    linuxAbsolutePathRegex.source,
    linuxPathStartsWithEnvVariableRegex.source,
    linuxPathStartsWithTildeRegex.source
  ].join('|'))
}

function buildValidRansomwarePathWindowsRegex() {
  return new RegExp([
    emptyRegex.source,
    windowsAbsolutePathRegex.source,
    windowsPathStartsWithEnvVariableRegex.source,
    windowsUncPathRegex.source
  ].join('|'))
}
