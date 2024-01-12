import { removeToken } from '@/_lib/authentication';
import { islandApiSlice } from '@/redux/features/api/islandApiSlice';

const logoutMiddleware = (store) => (next) => (action) => {
    if (action.type === 'LOGOUT') {
        removeToken();
        store.dispatch(islandApiSlice.util.resetApiState());
        window.dispatchEvent(new Event('LOGOUT'));
    }
    return next(action);
};

export default logoutMiddleware;
