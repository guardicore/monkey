import {
    localStorageGetItem,
    localStorageRemoveItem,
    localStorageSetItem
} from '@/_lib/localStorage';

enum StorageKeys {
    TOKEN = 'AuthenticationToken',
    LAST_REFRESH_TIMESTAMP = 'LastRefreshTimestamp',
    TTL = 'TokenTTL'
}

export const tokenStored = (): boolean => {
    const token = getToken();
    return token !== null;
};

export const getToken = (): string | null => {
    return localStorageGetItem(StorageKeys.TOKEN);
};

export const getTokenTTL = (): number | null => {
    const ttl = localStorageGetItem(StorageKeys.TTL);
    return ttl ? Number(ttl) : null;
};

export const setToken = (tokenValue: string, ttl: number) => {
    localStorageSetItem(StorageKeys.TTL, ttl);
    localStorageSetItem(StorageKeys.LAST_REFRESH_TIMESTAMP, Date.now());
    return localStorageSetItem(StorageKeys.TOKEN, tokenValue);
};

export const removeToken = () => {
    localStorageRemoveItem(StorageKeys.LAST_REFRESH_TIMESTAMP);
    localStorageRemoveItem(StorageKeys.TTL);
    return localStorageRemoveItem(StorageKeys.TOKEN);
};
