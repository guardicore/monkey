import {
    localStorageGetItem,
    localStorageSetItem,
    localStorageRemoveItem
} from '@/_lib/localStorage';
import {
    getToken,
    getTokenExpirationTime,
    setToken,
    removeToken,
    shouldRefreshToken,
    tokenStored,
    StorageKeys
} from './authentication';

const TOKEN = 'token';
const TTL = 12345;
const NOW = new Date('2020-01-01');
const YESTERDAY = new Date('2019-12-31');

jest.useFakeTimers();
jest.setSystemTime(NOW);
jest.mock('@/_lib/localStorage');
const localStorageValues = {};
const mockedLocalStorageGetItem = jest
    .mocked(localStorageGetItem)
    .mockImplementation((key: string) => {
        return localStorageValues[key];
    });
const mockedLocalStorageSetItem = jest.mocked(localStorageSetItem);
const mockedLocalStorageRemoveItem = jest.mocked(localStorageRemoveItem);

beforeEach(() => {
    localStorageValues[StorageKeys.TOKEN] = TOKEN;
    localStorageValues[StorageKeys.TTL] = TTL.toString();
    localStorageValues[StorageKeys.LAST_REFRESH_TIMESTAMP] = NOW.getTime();
    jest.clearAllMocks();
});

describe('authentication', () => {
    describe('getToken', () => {
        it('should get the token from local storage', () => {
            const token = getToken();
            expect(mockedLocalStorageGetItem).toHaveBeenCalled();
            expect(token).toBe('token');
        });
        it('should return null if there is no token in local storage', () => {
            localStorageValues[StorageKeys.TOKEN] = null;
            const token = getToken();
            expect(mockedLocalStorageGetItem).toHaveBeenCalled();
            expect(token).toBe(null);
        });
    });
    describe('getTokenExpirationTime', () => {
        it('should get the token ttl from local storage', () => {
            const ttl = getTokenExpirationTime();
            expect(mockedLocalStorageGetItem).toHaveBeenCalled();
            expect(ttl).toBe(NOW.getTime() + TTL);
        });
        it('should return null if there is no token ttl in local storage', () => {
            localStorageValues[StorageKeys.TTL] = null;
            const ttl = getTokenExpirationTime();
            expect(mockedLocalStorageGetItem).toHaveBeenCalled();
            expect(ttl).toBe(null);
        });
    });
    describe('setToken', () => {
        it('should set the token in local storage', () => {
            setToken(TOKEN, TTL);
            expect(mockedLocalStorageSetItem).toHaveBeenCalledWith(
                StorageKeys.TOKEN,
                TOKEN
            );
            expect(mockedLocalStorageSetItem).toHaveBeenCalledWith(
                StorageKeys.TTL,
                TTL
            );
            expect(mockedLocalStorageSetItem).toHaveBeenCalledWith(
                StorageKeys.LAST_REFRESH_TIMESTAMP,
                NOW.getTime()
            );
        });
    });
    describe('removeToken', () => {
        it('should remove the token from local storage', () => {
            removeToken();
            expect(mockedLocalStorageRemoveItem).toHaveBeenCalledWith(
                StorageKeys.TOKEN
            );
            expect(mockedLocalStorageRemoveItem).toHaveBeenCalledWith(
                StorageKeys.TTL
            );
            expect(mockedLocalStorageRemoveItem).toHaveBeenCalledWith(
                StorageKeys.LAST_REFRESH_TIMESTAMP
            );
        });
    });
    describe('tokenStored', () => {
        it('should return true if there is a token in local storage', () => {
            expect(tokenStored()).toBe(true);
        });
        it('should return false if there is no token in local storage', () => {
            localStorageValues[StorageKeys.TOKEN] = null;
            expect(tokenStored()).toBe(false);
        });
    });
    describe('shouldRefreshToken', () => {
        it('should return false if the last token refresh time could not be retrieved', () => {
            localStorageValues[StorageKeys.LAST_REFRESH_TIMESTAMP] = null;
            expect(shouldRefreshToken(true)).toBe(false);
        });
        it('should return false if the token ttl could not be retrieved', () => {
            localStorageValues[StorageKeys.TTL] = null;
            expect(shouldRefreshToken(true)).toBe(false);
        });
        it('should return false if the token is expired', () => {
            localStorageValues[StorageKeys.LAST_REFRESH_TIMESTAMP] =
                YESTERDAY.getTime();
            expect(shouldRefreshToken(true)).toBe(false);
        });
        it('should return false if the minimum refresh interval has not been reached', () => {
            expect(shouldRefreshToken(false, 10000)).toBe(false);
        });
        it('should return false if the user is not active', () => {
            expect(shouldRefreshToken(false)).toBe(false);
        });
        it('should return true in all other cases', () => {
            expect(shouldRefreshToken(true)).toBe(true);
        });
    });
});
