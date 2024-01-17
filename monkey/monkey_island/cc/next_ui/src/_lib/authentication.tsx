import {
    localStorageGetItem,
    localStorageRemoveItem,
    localStorageSetItem
} from '@/_lib/localStorage';

export enum StorageKeys {
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

/**
 * @returns The time in milliseconds when the token will expire.
 */
export const getTokenExpirationTime = (): number | null => {
    const ttl = localStorageGetItem(StorageKeys.TTL);
    const lastRefreshTimestamp = localStorageGetItem(
        StorageKeys.LAST_REFRESH_TIMESTAMP
    );
    if (!ttl || !lastRefreshTimestamp) {
        return null;
    }
    return Number(lastRefreshTimestamp) + Number(ttl);
};

/**
 * Get the amount of time that has passed since the token was last refreshed.
 * @returns The age of the token in milliseconds.
 */
export const getTokenAge = (): number | null => {
    const lastRefreshTimestamp = localStorageGetItem(
        StorageKeys.LAST_REFRESH_TIMESTAMP
    );
    if (!lastRefreshTimestamp) {
        return null;
    }
    return Date.now() - Number(lastRefreshTimestamp);
};

export const tokenExpired = (): boolean => {
    const expirationTime = getTokenExpirationTime();
    if (!expirationTime) {
        return true;
    }
    return expirationTime < Date.now();
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

/**
 * Whether or not the token should be refreshed.
 *
 * This is a combination of multiple factors:
 * - The token is not expired.
 * - The minimum refresh interval has passed.
 * - The user has been active within the refresh period.
 *
 * @param userIsActive Whether or not the user was active within this refresh period.
 * @param minimumRefreshInterval The minimum amount of time between refreshes, in milliseconds. Defaults to 0.
 * @returns true if the token should be refreshed, false otherwise.
 */
export const shouldRefreshToken = (
    userIsActive: boolean,
    minimumRefreshInterval: number = 0
) => {
    const tokenAge = getTokenAge();
    if (tokenAge === null) {
        return false;
    }
    if (tokenExpired()) {
        console.log('Token expired.');
        return false;
    }
    if (tokenAge < minimumRefreshInterval) {
        console.log('Token refreshed too recently.');
        return false;
    }
    if (!userIsActive) {
        console.log('User is not active.');
        return false;
    }
    return true;
};
