import { AuthenticationActions } from '@/redux/features/api/authentication/authenticationActions';
import { getTTL, tokenIsStored } from '@/_lib/authenticationToken';
import { setTimer } from '@/redux/features/api/authentication/authenticationTimerSlice';
import { store } from '@/redux/store';
import clearAuthenticationTimer from '@/redux/features/api/authentication/_lib/clearAuthenticationTimer';

const setAuthenticationTimer = () => {
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

export default setAuthenticationTimer;
