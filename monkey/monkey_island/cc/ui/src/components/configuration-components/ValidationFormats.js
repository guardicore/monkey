const ipRegex = '((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
const cidrNotationRegex = '([0-9]|1[0-9]|2[0-9]|3[0-2])'
const hostnameRegex = '^([A-Za-z0-9]*[A-Za-z]+[A-Za-z0-9]*.?)*([A-Za-z0-9]*[A-Za-z]+[A-Za-z0-9]*)$'
// path is empty, or starts with `/` OR `$`
const linuxDirRegex = '(^\\s*$)|^/|^\\$'
// path is empty, or starts like `C:\` OR `C:/` OR `$` OR `%abc%`
const windowsDirRegex = '(^\\s*$)|^([A-Za-z]:(\\\\|\\/))|^\\$|^(%\\w*\\d*\\s*%)'


export const IP_RANGE = 'ip-range';
export const IP = 'ip';
export const VALID_DIR_LINUX = 'valid-directory-linux'
export const VALID_DIR_WINDOWS = 'valid-directory-windows'

export const formValidationFormats = {
  [IP_RANGE]: buildIpRangeRegex(),
  [IP]: buildIpRegex(),
  [VALID_DIR_LINUX]: buildValidDirLinuxRegex(),
  [VALID_DIR_WINDOWS]: buildValidDirWindowsRegex()
};

function buildIpRangeRegex(){
  return new RegExp([
    '^'+ipRegex+'$|', // Single: IP
    '^'+ipRegex+'-'+ipRegex+'$|', // IP range: IP-IP
    '^'+ipRegex+'/'+cidrNotationRegex+'$|', // IP range with cidr notation: IP/cidr
    hostnameRegex // Hostname: target.tg
  ].join(''))
}

function buildIpRegex(){
  return new RegExp('^'+ipRegex+'$')
}

function buildValidDirLinuxRegex() {
  return new RegExp(linuxDirRegex)
}

function buildValidDirWindowsRegex() {
  return new RegExp(windowsDirRegex)
}
