import {
    localStorageGetItem,
    localStorageRemoveItem,
    localStorageSetItem
} from '@/_lib/localStorage';

const keyOfAuthenticationToken = 'AuthenticationToken';
const keyOfLastRefreshTimestamp = 'LastRefreshTimestamp';
const keyOfExpirationTimestamp = 'ExpirationTimestamp';

export const tokenStored = (): boolean => {
    const token = getToken();
    return token !== null;
};

export const getToken = (): string | null => {
    return localStorageGetItem(keyOfAuthenticationToken);
};

export const getTTL = (): number | null => {
    const now = Date.now();
    const expirationTimestamp = localStorageGetItem(keyOfExpirationTimestamp);
    if (expirationTimestamp === null) {
        return null;
    }
    return Number(expirationTimestamp) - now;
};

const TTLToTimestamp = (ttl: number): number => {
    const now = Date.now();
    return now + ttl;
};

export const setToken = (tokenValue: string, ttl: number) => {
    localStorageSetItem(keyOfExpirationTimestamp, TTLToTimestamp(ttl));
    localStorageSetItem(keyOfLastRefreshTimestamp, Date.now());
    return localStorageSetItem(keyOfAuthenticationToken, tokenValue);
};

export const removeToken = () => {
    localStorageRemoveItem(keyOfLastRefreshTimestamp);
    localStorageRemoveItem(keyOfExpirationTimestamp);
    return localStorageRemoveItem(keyOfAuthenticationToken);
};
