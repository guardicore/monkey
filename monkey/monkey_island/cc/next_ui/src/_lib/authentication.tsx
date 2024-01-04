import {
    localStorageGetItem,
    localStorageRemoveItem,
    localStorageSetItem
} from '@/_lib/localStorage.utils';

const keyOfAuthenticationToken = 'AuthenticationToken';
const keyOfLastRefreshTimestamp = 'LastRefreshTimestamp';
const keyOfTTL = 'TokenTTL';

export const isAuthenticated(): boolean {
    return !!getToken();
}

export const getToken(): string {
    return localStorageGetItem(keyOfAuthenticationToken);
}

export const setToken(tokenValue: string, ttl: number) {
    localStorageSetItem(keyOfTTL, ttl);
    localStorageSetItem(keyOfLastRefreshTimestamp, Date.now());
    return localStorageSetItem(keyOfAuthenticationToken, tokenValue);
}

export const removeToken() {
    localStorageRemoveItem(keyOfLastRefreshTimestamp);
    localStorageRemoveItem(keyOfTTL);
    return localStorageRemoveItem(keyOfAuthenticationToken);
}
