import {
    localStorageGetItem,
    localStorageSetItem,
    localStorageRemoveItem
} from '@/_lib/localStorage';
import {
    getToken,
    getTTL,
    setToken,
    removeToken,
    tokenStored,
    StorageKeys
} from './authentication';

const NOW = new Date('2020-01-01');

jest.useFakeTimers();
jest.setSystemTime(NOW);
jest.mock('@/_lib/localStorage');
const mockedLocalStorageGetItem = jest.mocked(localStorageGetItem);
const mockedLocalStorageSetItem = jest.mocked(localStorageSetItem);
const mockedLocalStorageRemoveItem = jest.mocked(localStorageRemoveItem);

describe('authentication', () => {
    describe('getToken', () => {
        it('should get the token from local storage', () => {
            mockedLocalStorageGetItem.mockReturnValue('token');
            const token = getToken();
            expect(mockedLocalStorageGetItem).toHaveBeenCalled();
            expect(token).toBe('token');
        });
        it('should return null if there is no token in local storage', () => {
            mockedLocalStorageGetItem.mockReturnValue(null);
            const token = getToken();
            expect(mockedLocalStorageGetItem).toHaveBeenCalled();
            expect(token).toBe(null);
        });
    });
    describe('getTTL', () => {
        it('should get the token expiration time from local storage', () => {
            mockedLocalStorageGetItem.mockReturnValue(
                (NOW.getTime() + 12345).toString()
            );
            const ttl = getTTL();
            expect(mockedLocalStorageGetItem).toHaveBeenCalled();
            expect(ttl).toBe(12345);
        });
        it('should return null if there is no token ttl in local storage', () => {
            mockedLocalStorageGetItem.mockReturnValue(null);
            const ttl = getTTL();
            expect(mockedLocalStorageGetItem).toHaveBeenCalled();
            expect(ttl).toBe(null);
        });
    });
    describe('setToken', () => {
        it('should set the token in local storage', () => {
            setToken('token', 12345);
            expect(mockedLocalStorageSetItem).toHaveBeenCalledWith(
                StorageKeys.TOKEN,
                'token'
            );
            expect(mockedLocalStorageSetItem).toHaveBeenCalledWith(
                expect.anything(),
                NOW.getTime() + 12345
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
                StorageKeys.EXPIRATION_TIMESTAMP
            );
            expect(mockedLocalStorageRemoveItem).toHaveBeenCalledWith(
                StorageKeys.LAST_REFRESH_TIMESTAMP
            );
        });
    });
    describe('tokenStored', () => {
        it('should return true if there is a token in local storage', () => {
            mockedLocalStorageGetItem.mockReturnValue('token');
            expect(tokenStored()).toBe(true);
        });
        it('should return false if there is no token in local storage', () => {
            mockedLocalStorageGetItem.mockReturnValue(null);
            expect(tokenStored()).toBe(false);
        });
    });
});
