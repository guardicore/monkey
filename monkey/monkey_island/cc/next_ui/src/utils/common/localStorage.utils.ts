export const isWindowDefined = (): boolean => {
    return typeof window !== 'undefined';
};

export const executeIfWindowDefined = (callback: () => void): any => {
    if (isWindowDefined()) {
        return callback();
    }
};

export const localStorageGetItem = (key: string): string | null => {
    const value: string | null = executeIfWindowDefined(() =>
        localStorage.getItem(key)
    );
    return value || null;
};

export const localStorageSetItem = (key: string, value: string): void => {
    executeIfWindowDefined(() => localStorage.setItem(key, value));
};

export const localStorageRemoveItem = (key: string): void => {
    executeIfWindowDefined(() => localStorage.removeItem(key));
};
