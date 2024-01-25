import IAuthenticationRepository from './IAuthenticationRepository';
import { authenticationEndpoints } from '@/redux/features/api/authentication/authenticationEndpoints';
import { ThunkDispatch, AnyAction, Store } from '@reduxjs/toolkit';

type DispatchFunctionType = ThunkDispatch<any, undefined, AnyAction>;

class RTKAuthenticationRepository implements IAuthenticationRepository {
    store: Store & { dispatch: DispatchFunctionType };

    constructor(store: Store & { dispatch: DispatchFunctionType }) {
        this.store = store;
    }

    async login(username, password) {
        try {
            await this.store
                .dispatch(
                    authenticationEndpoints.endpoints.login.initiate({
                        username,
                        password
                    })
                )
                .unwrap();
            return { isError: false, error: null };
        } catch (e) {
            console.log('Got error: ', e);
            return { isError: true, error: e.data.response };
        }
    }

    async register(username, password) {
        const registerPromise = this.store.dispatch(
            authenticationEndpoints.endpoints.register.initiate({
                username,
                password
            })
        );
        // const { refetch } = loginPromise;
        const { isError, error } = await registerPromise;
        return { isError, error };
    }

    async logout() {
        const logoutPromise = this.store.dispatch(
            authenticationEndpoints.endpoints.logout.initiate()
        );
        const { isError, error } = await logoutPromise;
        return { isError, error };
    }
}

export default RTKAuthenticationRepository;
