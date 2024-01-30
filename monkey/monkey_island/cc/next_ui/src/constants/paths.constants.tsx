export enum PATHS {
    HOME = '/home',
    MAP = '/map',
    EVENTS = '/events',
    REGISTRATION = '/registration',
    LOGIN = '/login',
    ROOT = '/'
}

export const getApiPath = () => {
    if (typeof window !== 'undefined') {
        return location.protocol + '//' + location.host + '/api';
    }
};
