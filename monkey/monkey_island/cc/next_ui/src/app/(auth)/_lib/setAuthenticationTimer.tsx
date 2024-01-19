import { AuthenticationActions } from '@/redux/features/api/authentication/authenticationActions';
import { getTTL, tokenStored } from '@/_lib/authentication';
import { setTimer } from '@/redux/features/api/authenticationTimerSlice';
import { store } from '@/redux/store';
import clearAuthenticationTimer from '@/app/(auth)/_lib/clearAuthenticationTimer';

const setAuthenticationTimer = () => {
    const tokenTTL = getTTL();

    if (!tokenStored()) {
        return;
    }

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
