import {
    localStorageGetItem,
    localStorageRemoveItem,
    localStorageSetItem
} from '@/lib/localStorage';

export enum StorageKeys {
    TOKEN = 'AuthenticationToken',
    LAST_REFRESH_TIMESTAMP = 'LastRefreshTimestamp',
    EXPIRATION_TIMESTAMP = 'ExpirationTimestamp'
}

export const tokenStored = (): boolean => {
    const token = getToken();
    return token !== null;
};

export const getToken = (): string | null => {
    return localStorageGetItem(StorageKeys.TOKEN);
};

export const getTTL = (): number | null => {
    const now = Date.now();
    const expirationTimestamp = localStorageGetItem(
        StorageKeys.EXPIRATION_TIMESTAMP
    );
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
    localStorageSetItem(StorageKeys.EXPIRATION_TIMESTAMP, TTLToTimestamp(ttl));
    localStorageSetItem(StorageKeys.LAST_REFRESH_TIMESTAMP, Date.now());
    return localStorageSetItem(StorageKeys.TOKEN, tokenValue);
};

export const removeToken = () => {
    localStorageRemoveItem(StorageKeys.LAST_REFRESH_TIMESTAMP);
    localStorageRemoveItem(StorageKeys.EXPIRATION_TIMESTAMP);
    return localStorageRemoveItem(StorageKeys.TOKEN);
};
