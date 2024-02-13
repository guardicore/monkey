export enum PATHS {
    ABOUT = '/about',
    CONFIGURE = '/configure',
    LOGIN = '/login',
    NETWORK_MAP = '/network-map',
    REGISTRATION = '/registration',
    REPORT = '/report',
    PLUGINS = '/plugins',
    ROOT = '/',
    RUN = '/run'
}

export const getApiPath = () => {
    if (typeof window !== 'undefined') {
        return location.protocol + '//' + location.host + '/api';
    }
};
