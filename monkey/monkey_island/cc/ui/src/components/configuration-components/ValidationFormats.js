const ipRegex = '((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
const cidrNotationRegex = '([0-9]|1[0-9]|2[0-9]|3[0-2])'
const hostnameRegex = '^([A-Za-z0-9]*[A-Za-z]+[A-Za-z0-9]*.?)*([A-Za-z0-9]*[A-Za-z]+[A-Za-z0-9]*)$'

export const IP_RANGE = 'ip-range';
export const IP = 'ip';

export const formValidationFormats = {
  [IP_RANGE]: buildIpRangeRegex(),
  [IP]: buildIpRegex()
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
