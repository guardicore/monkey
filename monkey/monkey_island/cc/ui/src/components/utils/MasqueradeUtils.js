const MASQUERADE_TEXTS_PREFIX = 'InfectionMonkeyTextsMasquePrefix\0';
const MASQUERADE_BYTES_PREFIX = 'InfectionMonkeyBase64MasquePrefix\0';
const ENCODING = 'utf-8';
const NULL_BYTE = '\0';
const OS_TYPES = ['linux', 'windows'];
const MASQUE_TYPES = ['masque_texts', 'masque_base64']

export const MASQUERADE_TYPE_PREFIX = {
  TEXTS: MASQUERADE_TEXTS_PREFIX,
  BASE64: MASQUERADE_BYTES_PREFIX
}

// TODO: change
export function transformStringsToBytes(stringsArray, masqueTypePrefix) {
  if (stringsArray.length > 0) {
    const encoder = new TextEncoder(ENCODING);

    let bytes = stringsArray
      .map(str => str ? encoder.encode((masqueTypePrefix === MASQUERADE_TYPE_PREFIX.BASE64 ? base64ToText(str) : str) + NULL_BYTE) : [])
      .reduce((accumulator, currentString) => [...accumulator, ...currentString], []);

    let prefixBytes = encoder.encode(masqueTypePrefix);
    return new Uint8Array([...prefixBytes, ...bytes]);
  }

  return [];
}

// TODO: change -
export function getStringsFromBytes(bytesArray, masqueTypePrefix) {
  const encoder = new TextEncoder(ENCODING);
  const decoder = new TextDecoder(ENCODING);
  const prefixBytes = encoder.encode(masqueTypePrefix);
  const prefixIndex = getPrefixIndexFromBytesArray(bytesArray, prefixBytes);

  if (prefixIndex === -1) {
    return [];
  }

  const dataViewArray = new DataView(bytesArray, prefixIndex + prefixBytes.length);
  const stringsBytes = decoder.decode(dataViewArray);
  let stringsArray = stringsBytes.split(NULL_BYTE);

  if (masqueTypePrefix === MASQUERADE_TYPE_PREFIX.BASE64) {
    stringsArray = stringsArray.map(str => {
      return textToBase64(str);
    })
  }
  return stringsArray.filter(str => str !== '');
}

function getPrefixIndexFromBytesArray(bytesArray, prefix) {
  // const uint8Array = new Uint8Array(bytesArray);
  console.log(bytesArray);
  console.log(bytesArray);
  return bytesArray.findIndex((_value, index) => {
    for (let i = 0; i < prefix.length; i++) {
      if (bytesArray[index + i] !== prefix[i]) {
        return false;
      }
    }
    return true;
  });
}

const base64ToText = (base64) => {
  // Convert the base64 string to a byte array
  const bytes = atob(base64)
    .split('')
    .map((char) => char.charCodeAt(0));

  // Create a new TextDecoder object to decode the byte array to a string
  const decoder = new TextDecoder('utf-8');
  return decoder.decode(new Uint8Array(bytes));
}


// TODO: The server should return a base64 string
const textToBase64 = (text) => {
  const encoder = new TextEncoder(ENCODING);

  const uint8Array = encoder.encode(text);

  // Convert the Uint8Array to a base64-encoded string
  const base64String = btoa(String.fromCharCode(...uint8Array));

  return base64String;
}

export const getMasqueradesBytesArrays = (masqueStrings) => {
  let linuxMasqueBytes = [], windowsMasqueBytes = [];

  OS_TYPES.forEach(osType => {
    let bytesArray = []

    MASQUE_TYPES.forEach(masqueType => {
      let kuku = MASQUERADE_TYPE_PREFIX.TEXTS;
      if (masqueType === 'masque_texts') {
        kuku = MASQUERADE_TYPE_PREFIX.TEXTS;
      } else {
        kuku = MASQUERADE_TYPE_PREFIX.BASE64;
      }

      bytesArray = [...bytesArray, ...transformStringsToBytes(masqueStrings?.[osType]?.[masqueType], kuku)]
    })

    if (osType === 'linux') {
      linuxMasqueBytes = [...bytesArray];
    } else if (osType === 'windows') {
      windowsMasqueBytes = [...bytesArray];
    }
  })

  return {linuxMasqueBytes, windowsMasqueBytes};
}
