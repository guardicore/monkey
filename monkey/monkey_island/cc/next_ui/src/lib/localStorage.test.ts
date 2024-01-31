import {
    isWindowDefined,
    executeIfWindowDefined,
    localStorageGetItem,
    localStorageSetItem,
    localStorageRemoveItem
} from '@/lib/localStorage';

const windowMock = jest.spyOn(globalThis, 'window', 'get');
let mockData = {};

beforeAll(() => {
    global.Storage.prototype.setItem = jest.fn((key: string, value) => {
        mockData[key] = value;
    });
    global.Storage.prototype.getItem = jest.fn((key: string) => mockData[key]);
    global.Storage.prototype.removeItem = jest.fn(() => {});
});

afterAll(() => {
    // @ts-ignore
    global.Storage.prototype.setItem.mockReset();
    // @ts-ignore
    global.Storage.prototype.getItem.mockReset();
    // @ts-ignore
    global.Storage.prototype.removeItem.mockReset();
});

beforeEach(() => {
    mockData = {};
    // jest.clearAllMocks();

    windowMock.mockClear();
    // @ts-ignore
    windowMock.mockReturnValue({});
});

describe('localStorage', () => {
    describe('localStorageGetItem', () => {
        it('should get the item from local storage', () => {
            mockData['key'] = 'value';
            const item = localStorageGetItem('key');
            expect(item).toBe('value');
        });
        it('should return null if there is no item in local storage', () => {
            const item = localStorageGetItem('key');
            expect(item).toBe(null);
        });
        it('should return null if the window is not defined', () => {
            // @ts-ignore
            windowMock.mockReturnValue(undefined);
            const item = localStorageGetItem('key');
            expect(item).toBe(null);
        });
    });
    describe('localStorageSetItem', () => {
        it('should set the item in local storage', () => {
            localStorageSetItem('key', 'value');
            expect(mockData['key']).toBe('value');
        });
        // TODO: Should it silently fail if there is no window?
    });
    describe('localStorageRemoveItem', () => {
        it('should remove the item from local storage', () => {
            localStorageRemoveItem('key');
            expect(localStorage.removeItem).toHaveBeenCalledWith('key');
        });
        // TODO: Should it silently fail if there is no window?
    });
    describe('isWindowDefined', () => {
        it('should return true if window is defined', () => {
            expect(isWindowDefined()).toBe(true);
        });
        it('should return false if window is not defined', () => {
            // @ts-ignore
            windowMock.mockReturnValue(undefined);
            expect(isWindowDefined()).toBe(false);
        });
    });
    describe('executeIfWindowDefined', () => {
        it('should execute the callback if window is defined', () => {
            // @ts-ignore
            windowMock.mockReturnValue({});
            const callback = jest.fn();
            executeIfWindowDefined(callback);
            expect(callback).toHaveBeenCalled();
        });
        it('should not execute the callback if window is not defined', () => {
            // @ts-ignore
            windowMock.mockReturnValue(undefined);
            const callback = jest.fn();
            executeIfWindowDefined(callback);
            expect(callback).not.toHaveBeenCalled();
        });
    });
});
