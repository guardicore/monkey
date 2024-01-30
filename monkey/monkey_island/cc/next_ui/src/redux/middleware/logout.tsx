import { removeToken } from '@/lib/authenticationToken';
import { islandApiSlice } from '@/redux/features/api/islandApiSlice';
import { Events } from '@/constants/events.constants';
import { AuthenticationActions } from '@/redux/features/api/authentication/authenticationActions';

import { clearAuthenticationTimer } from '@/redux/features/api/authentication/lib/authenticationTimer';

const logoutMiddleware = (store) => (next) => (action) => {
    if (action.type === AuthenticationActions.logout.type) {
        removeToken();
        clearAuthenticationTimer();
        store.dispatch(islandApiSlice.util.resetApiState());
        window.dispatchEvent(new Event(Events.LOGOUT));
    }
    return next(action);
};

export default logoutMiddleware;
