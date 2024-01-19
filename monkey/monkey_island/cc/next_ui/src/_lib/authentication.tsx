import {
    localStorageGetItem,
    localStorageRemoveItem,
    localStorageSetItem
} from '@/_lib/localStorage';

const keyOfAuthenticationToken = 'AuthenticationToken';
const keyOfLastRefreshTimestamp = 'LastRefreshTimestamp';
const keyOfTTL = 'TokenTTL';

export const tokenStored = (): boolean => {
    const token = getToken();
    return token !== null;
};

export const getToken = (): string | null => {
    return localStorageGetItem(keyOfAuthenticationToken);
};

export const getTTL = (): number | null => {
    return localStorageGetItem(keyOfTTL);
};

export const setToken = (tokenValue: string, ttl: number) => {
    localStorageSetItem(keyOfTTL, ttl);
    localStorageSetItem(keyOfLastRefreshTimestamp, Date.now());
    return localStorageSetItem(keyOfAuthenticationToken, tokenValue);
};

export const removeToken = () => {
    localStorageRemoveItem(keyOfLastRefreshTimestamp);
    localStorageRemoveItem(keyOfTTL);
    return localStorageRemoveItem(keyOfAuthenticationToken);
};
