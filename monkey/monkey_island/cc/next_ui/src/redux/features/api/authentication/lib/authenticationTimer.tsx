import { AuthenticationActions } from '@/redux/features/api/authentication/authenticationActions';
import { getTTL, tokenIsStored } from '@/lib/authenticationToken';
import {
    clearTimer,
    setTimer
} from '@/redux/features/api/authentication/authenticationTimerSlice';
import { store } from '@/redux/store';
import _ from 'lodash';

export const clearAuthenticationTimer = () => {
    const storedTimer = _.cloneDeep(store.getState().authenticationTimer.timer);
    if (storedTimer !== null) {
        clearTimeout(storedTimer);
    }
    store.dispatch(clearTimer());
};

export const setAuthenticationTimer = () => {
    if (!tokenIsStored()) {
        return;
    }

    const tokenTTL = getTTL();
    if (tokenTTL === null) {
        store.dispatch(AuthenticationActions.logout);
        throw Error("Token TTL is not defined, can't start logout timer");
    }

    const authenticationTimer = setTimeout(() => {
        store.dispatch(AuthenticationActions.logout);
    }, tokenTTL);

    clearAuthenticationTimer();
    store.dispatch(setTimer(authenticationTimer));
};
