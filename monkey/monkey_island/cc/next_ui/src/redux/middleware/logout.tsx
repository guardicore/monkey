import { removeToken } from '@/_lib/authentication';
import { islandApiSlice } from '@/redux/features/api/islandApiSlice';
import { Events } from '@/constants/events.constants';
import { AuthenticationActions } from '@/redux/features/api/authentication/authenticationActions';

const logoutMiddleware = (store) => (next) => (action) => {
    if (action.type === AuthenticationActions.logout) {
        removeToken();
        store.dispatch(islandApiSlice.util.resetApiState());
        window.dispatchEvent(new Event(Events.LOGOUT));
    }
    return next(action);
};

export default logoutMiddleware;
