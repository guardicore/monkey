const MASQUERADE_STRINGS_PREFIX = 'InfectionMonkeyMasquePrefix';

export function transformStringsToBytes(stringsArray){
  const encoder = new TextEncoder('utf-8');

  let bytes = stringsArray
    .map(str => str ? encoder.encode(str + '\0') : [])
    .reduce((accumulator, currentString) => [...accumulator, ...currentString], []);

  let prefixBytes = encoder.encode(MASQUERADE_STRINGS_PREFIX);
  return new Uint8Array([...prefixBytes, ...bytes]);
}

export function getStringsFromBytes(bytesArray) {
  const encoder = new TextEncoder('utf-8');
  const decoder = new TextDecoder('utf-8');
  const prefixBytes = encoder.encode(MASQUERADE_STRINGS_PREFIX);
  const prefixIndex = getPrefixIndexFromBytesArray(bytesArray, prefixBytes);
  if (prefixIndex === -1) {
    return [];
  }
  const dataViewArray = new DataView(bytesArray, prefixIndex + prefixBytes.length);
  const stringsBytes = decoder.decode(dataViewArray);
  const stringsArray = stringsBytes.split('\0');

  return stringsArray.filter(str => str !== '');
}

function getPrefixIndexFromBytesArray(bytesArray, prefix){
  const uint8Array = new Uint8Array(bytesArray);
  return uint8Array.findIndex((_value, index) => {
  for (let i = 0; i < prefix.length; i++) {
    if (uint8Array[index + i] !== prefix[i]) {
      return false;
    }
  }
  return true;
  });
}
