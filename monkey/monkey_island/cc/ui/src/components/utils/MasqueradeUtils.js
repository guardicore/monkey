import { cloneDeep } from 'lodash';
import { DEFAULT_MASQUES_VALUES } from '../../services/configuration/masquerade';

const NULL_BYTE = '\0';
const MASQUERADE_TEXTS_PREFIX = `InfectionMonkeyTextsMasquePrefix${NULL_BYTE}`;
const MASQUERADE_BASE64_PREFIX = `InfectionMonkeyBase64MasquePrefix${NULL_BYTE}`;
const ENCODING_FORMAT = 'utf-8';

const OS_TYPES = ['linux', 'windows'];

export const MASQUE_TYPES = {
    TEXTS: { key: 'masque_texts', prefix: MASQUERADE_TEXTS_PREFIX },
    BASE64: { key: 'masque_base64', prefix: MASQUERADE_BASE64_PREFIX }
};

var base64 = require('base64-js');

export function transformStringsToBytes(stringsArray, masquePrefix) {
    if (stringsArray?.length) {
        let bytes = [];
        if (masquePrefix === MASQUE_TYPES.TEXTS.prefix) {
            bytes = stringsArray
                .map((str) => (str ? encodeString(str + NULL_BYTE) : []))
                .reduce((accumulator, currentString) => [...accumulator, ...currentString], []);
        } else {
            bytes = base64ToBytes(stringsArray[0]);
        }
        let prefixBytes = encodeString(masquePrefix);
        return new Uint8Array([...prefixBytes, ...bytes]);
    }

    return [];
}

export function getStringsFromBytes(bytesArray, masqueType, masqueDetails) {
    if (bytesArray && bytesArray?.byteLength && masqueDetails) {
        const dataViewArray = new DataView(
            bytesArray,
            masqueDetails.offsetIndex + masqueDetails.prefixLength,
            masqueDetails.length
        );
        const stringsBytes = decodeBytes(dataViewArray);
        let stringsArray = stringsBytes.split(NULL_BYTE);

        if (masqueType.key === MASQUE_TYPES.TEXTS.key) {
            return stringsArray.filter((str) => str !== '');
        }

        // In order to support only one base64's textarea
        var uint8Array = splitUint8ArrayByNull(new Uint8Array(dataViewArray.buffer)).slice(-1)[0];
        return bytesToBase64(uint8Array) || getDefaultValueByMasquePrefix(masqueType.key);
    }

    return getDefaultValueByMasquePrefix(masqueType.key);
}

function splitUint8ArrayByNull(uint8Array) {
    var subarrays = [];
    var startIndex = 0;

    for (var i = 0; i < uint8Array.length; i++) {
        if (uint8Array[i] === 0x00) {
            subarrays.push(uint8Array.slice(startIndex, i));
            startIndex = i + 1;
        }
    }

    // Push the remaining portion after the last null byte (if any)
    if (startIndex < uint8Array.length) {
        subarrays.push(uint8Array.slice(startIndex));
    }

    return subarrays;
}

const getDefaultValueByMasquePrefix = (masqueType) => {
    return Object.entries(cloneDeep(DEFAULT_MASQUES_VALUES)).filter(([key, _defaultValue]) => {
        return masqueType?.includes(key);
    })?.[0]?.[1];
};

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

const base64ToBytes = (base64String) => {
    var bytes = base64.toByteArray(base64String);
    return bytes;
};

const bytesToBase64 = (bytes) => {
    var base64String = base64.fromByteArray(bytes);
    return base64String;
};

export const getMasqueradesBytesArrays = (masqueStrings) => {
    let linuxMasqueBytes = new Uint8Array([]),
        windowsMasqueBytes = new Uint8Array([]);

    OS_TYPES.forEach((osType) => {
        let bytesArray = [];

        Object.values(MASQUE_TYPES).forEach(({ key, prefix }) => {
            let currentVal = cloneDeep(masqueStrings?.[osType]?.[key]);
            // If it's a single value, and it's not empty, convert it to array with this one item
            if (!Array.isArray(currentVal)) {
                currentVal = currentVal ? [currentVal] : [];
            }

            bytesArray = [...bytesArray, ...transformStringsToBytes(currentVal, prefix)];
        });

        if (osType === 'linux') {
            linuxMasqueBytes = new Uint8Array([...bytesArray]);
        } else if (osType === 'windows') {
            windowsMasqueBytes = new Uint8Array([...bytesArray]);
        }
    });

    return { linuxMasqueBytes, windowsMasqueBytes };
};

export const getMasqueradeBytesSubsets = (bytesArray) => {
    let subsetsDetails = {};
    const defaultValues = { offsetIndex: null, prefixLength: null, length: null };

    const masqueTypesValues = Object.values(MASQUE_TYPES);

    masqueTypesValues.forEach(({ key, prefix }) => {
        const prefixBytes = encodeString(prefix);
        let offsetIndex = getPrefixIndexFromBytesArray(bytesArray, prefixBytes);

        if (offsetIndex !== -1) {
            subsetsDetails[key] = { ...defaultValues };
            subsetsDetails[key].offsetIndex = offsetIndex;
            subsetsDetails[key].prefixLength = prefix.length;
        }
    });

    if (bytesArray?.byteLength && Object.keys(subsetsDetails).length === 0) {
        subsetsDetails[MASQUE_TYPES.BASE64.key] = Object.assign(
            { ...defaultValues },
            { offsetIndex: 0 }
        );
    }

    subsetsDetails = calculateMasquesSubsetsLengths(subsetsDetails, bytesArray.byteLength);
    return subsetsDetails;
};

const calculateMasquesSubsetsLengths = (subsetsDetails, bytesArrayLength) => {
    const subsetsDetailsToReturn = cloneDeep(subsetsDetails);
    const keys = Object.keys(subsetsDetailsToReturn).sort(
        (a, b) => subsetsDetailsToReturn[a].offsetIndex - subsetsDetailsToReturn[b].offsetIndex
    );
    for (let i = 0; i < keys.length; i++) {
        const key = keys[i];
        const obj = subsetsDetailsToReturn[key];
        const subsetOffset = obj.offsetIndex + (obj?.prefixLength || 0);
        if (i < keys.length - 1) {
            obj.length = Math.abs(subsetOffset - subsetsDetailsToReturn[keys[i + 1]].offsetIndex);
        } else {
            obj.length = bytesArrayLength - subsetOffset;
        }
    }
    return subsetsDetailsToReturn;
};

const encodeString = (str) => {
    const encoder = new TextEncoder(ENCODING_FORMAT);
    return encoder.encode(str);
};

const decodeBytes = (bytes) => {
    const decoder = new TextDecoder(ENCODING_FORMAT);
    return decoder.decode(bytes);
};
