export enum PATHS {
    HOME = '/home',
    MAP = '/map',
    EVENTS = '/events',
    SIGN_IN = '/signin',
    SIGN_UP = '/signup',
    ROOT = '/'
}

export const AUTHENTICATION_PATHS = [PATHS.SIGN_IN, PATHS.SIGN_UP];

export const getApiPath = () => {
    if (typeof window !== 'undefined') {
        return location.protocol + '//' + location.host + '/api';
    }
};
