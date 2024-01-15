import { HTTP_METHODS } from '@/constants/http.constants';
import {
    EndpointBuilder,
    QueryFulfilledRejectionReason
} from '@reduxjs/toolkit/dist/query/endpointDefinitions';
import { islandApiSlice } from '@/redux/features/api/islandApiSlice';
import { LoginParams } from '@/redux/features/api/types/islandApi';
import handleAuthToken from '@/app/(auth)/_lib/handleAuthToken';
import { PromiseWithKnownReason } from '@reduxjs/toolkit/dist/query/core/buildMiddleware/types';
import { AuthenticationActions } from '@/redux/features/api/authentication/authenticationActions';

enum BackendEndpoints {
    LOGIN = '/login',
    REGISTER = '/register',
    LOGOUT = '/logout'
}

async function handleTokenResponse(
    queryFulfilled: PromiseWithKnownReason<
        { data: any; meta: any },
        QueryFulfilledRejectionReason<any>
    >
) {
    try {
        const { data } = await queryFulfilled;
        handleAuthToken(data);
    } catch (error) {
        // dispatch();
    }
}

export const authenticationEndpoints = islandApiSlice.injectEndpoints({
    endpoints: (builder: EndpointBuilder<any, any, any>) => ({
        login: builder.mutation<void, LoginParams>({
            query: (loginValues) => ({
                url: BackendEndpoints.LOGIN,
                method: HTTP_METHODS.POST,
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(loginValues)
            }),
            async onQueryStarted(_, { queryFulfilled }) {
                await handleTokenResponse(queryFulfilled);
            }
        }),
        register: builder.mutation<void, LoginParams>({
            query: (loginValues) => ({
                url: BackendEndpoints.REGISTER,
                method: HTTP_METHODS.POST,
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(loginValues)
            }),
            async onQueryStarted(_, { queryFulfilled }) {
                await handleTokenResponse(queryFulfilled);
            }
        }),
        logout: builder.mutation<void, void>({
            query: () => ({
                url: BackendEndpoints.LOGOUT,
                method: HTTP_METHODS.POST,
                headers: {
                    'Content-Type': 'application/json'
                }
            }),
            async onQueryStarted(_, { dispatch, queryFulfilled }) {
                try {
                    await queryFulfilled;
                    dispatch(AuthenticationActions.logout);
                } catch (error) {
                    // dispatch();
                }
            }
        })
    })
});

export const { useLoginMutation, useRegisterMutation, useLogoutMutation } =
    authenticationEndpoints;
