import {cloneDeep} from 'lodash';

const MASQUERADE_TEXTS_PREFIX = 'InfectionMonkeyTextsMasquePrefix\0';
const MASQUERADE_BASE64_PREFIX = 'InfectionMonkeyBase64MasquePrefix\0';
const ENCODING = 'utf-8';
const NULL_BYTE = '\0';
const OS_TYPES = ['linux', 'windows'];

export const MASQUE_TYPES = {
  TEXTS: {key: 'masque_texts', prefix: MASQUERADE_TEXTS_PREFIX},
  BASE64: {key: 'masque_base64', prefix: MASQUERADE_BASE64_PREFIX}
}

export function transformStringsToBytes(stringsArray, masquePrefix) {
  if (stringsArray.length > 0) {
    let bytes = stringsArray
      .map(str => str ? encodeString((masquePrefix === MASQUE_TYPES.BASE64.prefix ? base64ToText(str) : str) + NULL_BYTE) : [])
      .reduce((accumulator, currentString) => [...accumulator, ...currentString], []);

    let prefixBytes = encodeString(masquePrefix);
    return new Uint8Array([...prefixBytes, ...bytes]);
  }

  return [];
}

export function getStringsFromBytes(bytesArray, masquePrefix, masqueDetails) {
  if (bytesArray && masqueDetails) {
    const dataViewArray = new DataView(bytesArray, masqueDetails.offsetIndex + masqueDetails.prefixLength, masqueDetails.length);
    const stringsBytes = decodeBytes(dataViewArray);
    let stringsArray = stringsBytes.split(NULL_BYTE);

    if (masquePrefix === MASQUE_TYPES.BASE64.prefix) {
      stringsArray = stringsArray.map(str => {
        return textToBase64(str);
      })
    }
    return stringsArray.filter(str => str !== '');
  }

  return [];
}

function getPrefixIndexFromBytesArray(bytesArray, prefix) {
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

const base64ToText = (base64) => {
  // Convert the base64 string to a byte array
  const bytes = atob(base64)
    .split('')
    .map((char) => char.charCodeAt(0));

  return decodeBytes(new Uint8Array(bytes));
}

const textToBase64 = (text) => {
  const uint8Array = encodeString(text);

  // Convert the Uint8Array to a base64-encoded string
  const base64String = btoa(String.fromCharCode(...uint8Array));

  return base64String;
}

export const getMasqueradesBytesArrays = (masqueStrings) => {
  let linuxMasqueBytes = new Uint8Array([]), windowsMasqueBytes = new Uint8Array([]);

  OS_TYPES.forEach(osType => {
    let bytesArray = []

    Object.values(MASQUE_TYPES).forEach(({key, prefix}) => {
      bytesArray = [...bytesArray, ...transformStringsToBytes(masqueStrings?.[osType]?.[key], prefix)]
    });

    if (osType === 'linux') {
      linuxMasqueBytes = new Uint8Array([...bytesArray]);
    } else if (osType === 'windows') {
      windowsMasqueBytes = new Uint8Array([...bytesArray]);
    }
  })

  return {linuxMasqueBytes, windowsMasqueBytes};
}

export const getMasqueradeBytesSubsets = (bytesArray) => {
  let subsetsDetails = {};
  const defaultValues = {offsetIndex: null, prefixLength: null, length: null};

  const masqueTypesValues = Object.values(MASQUE_TYPES);

  masqueTypesValues.forEach(({key, _prefix}) => {
    subsetsDetails[key] = {...defaultValues};
  });

  masqueTypesValues.forEach(({key, prefix}) => {
    const prefixBytes = encodeString(prefix);
    let offsetIndex = getPrefixIndexFromBytesArray(bytesArray, prefixBytes);

    if (offsetIndex !== -1) {
      subsetsDetails[key].offsetIndex = offsetIndex;
      subsetsDetails[key].prefixLength = prefix.length;
    }
  });

  subsetsDetails = filterOutSubsetWithNullOffsetIndex(subsetsDetails);
  subsetsDetails = calculateMasquesSubsetsLengths(subsetsDetails, bytesArray.byteLength)
  return subsetsDetails;
}

const filterOutSubsetWithNullOffsetIndex = (subsetsDetails) => {
  const filteredSubsets = {};
  for (const key in subsetsDetails) {
    if (subsetsDetails[key].offsetIndex !== null) {
      filteredSubsets[key] = subsetsDetails[key];
    }
  }
  return filteredSubsets;
}

const calculateMasquesSubsetsLengths = (subsetsDetails, bytesArrayLength) => {
  const subsetsDetailsToReturn = cloneDeep(subsetsDetails);
  const keys = Object.keys(subsetsDetailsToReturn).sort((a, b) => subsetsDetailsToReturn[a].offsetIndex - subsetsDetailsToReturn[b].offsetIndex);
  for (let i = 0; i < keys.length; i++) {
    const key = keys[i];
    const obj = subsetsDetailsToReturn[key];
    const subsetOffset = obj.offsetIndex + obj.prefixLength;
    if (i < keys.length - 1) {
      obj.length = Math.abs(subsetOffset - subsetsDetailsToReturn[keys[i + 1]].offsetIndex);
    } else {
      obj.length = bytesArrayLength - subsetOffset;
    }
  }
  return subsetsDetailsToReturn;
};


const encodeString = str => {
   const encoder = new TextEncoder(ENCODING);
   return encoder.encode(str);
}

const decodeBytes = bytes => {
   const decoder = new TextDecoder(ENCODING);
   return decoder.decode(bytes);
}
