export const getCurrentTimestamp = (): number => {
    return Date.now();
};

export const getCurrentTimestampInSeconds = (): number => {
    return getCurrentTimestamp() / 1000;
};
