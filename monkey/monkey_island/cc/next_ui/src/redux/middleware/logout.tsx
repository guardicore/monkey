import { removeToken } from '@/_lib/authentication';
import { islandApiSlice } from '@/redux/features/api/islandApiSlice';
import { Actions } from '@/redux/features/actions';
import { Events } from '@/constants/events.constants';

const logoutMiddleware = (store) => (next) => (action) => {
    if (action.type === Actions.LOGOUT) {
        removeToken();
        store.dispatch(islandApiSlice.util.resetApiState());
        window.dispatchEvent(new Event(Events.LOGOUT));
    }
    return next(action);
};

export default logoutMiddleware;
