import { HTTP_METHODS } from '@/constants/http.constants';
import { EndpointBuilder } from '@reduxjs/toolkit/dist/query/endpointDefinitions';
import { islandApiSlice } from '@/redux/features/api/islandApiSlice';
import { LoginParams } from '@/redux/features/api/types/islandApi';
import { AuthenticationActions } from '@/redux/features/api/authentication/authenticationActions';

enum BackendEndpoints {
    LOGIN = '/login',
    REGISTER = '/register',
    LOGOUT = '/logout',
    REGISTRATION_STATUS = '/registration-status'
}

interface apiLoginResponse {
    response?: {
        user: {
            authentication_token: string;
            token_ttl_sec: number;
        };
    };
    data?: {
        response: {
            errors: string[];
        };
    };
}
export type ErrorResponse = string[];
export interface SuccessfulAuthenticationResponse {
    authenticationToken: string;
    tokenTTLSeconds: number;
}

export interface RegistrationStatusResponse {
    registrationNeeded: boolean;
}

export const authenticationEndpoints = islandApiSlice.injectEndpoints({
    endpoints: (builder: EndpointBuilder<any, any, any>) => ({
        login: builder.mutation<SuccessfulAuthenticationResponse, LoginParams>({
            query: (loginValues) => ({
                url: BackendEndpoints.LOGIN,
                method: HTTP_METHODS.POST,
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(loginValues)
            }),
            transformResponse: (
                response: apiLoginResponse
            ): SuccessfulAuthenticationResponse => {
                const authData = response.response?.user;
                if (!authData) {
                    throw new Error(
                        "Can't find authentication data in server's response"
                    );
                }
                return {
                    authenticationToken: authData.authentication_token,
                    tokenTTLSeconds: authData.token_ttl_sec
                };
            },
            transformErrorResponse: (response): ErrorResponse => {
                return response.data.response.errors;
            }
        }),
        register: builder.mutation<
            SuccessfulAuthenticationResponse,
            LoginParams
        >({
            query: (loginValues) => ({
                url: BackendEndpoints.REGISTER,
                method: HTTP_METHODS.POST,
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(loginValues)
            }),
            transformResponse: (response): SuccessfulAuthenticationResponse => {
                const authData = response.response?.user;
                if (!authData) {
                    throw new Error(
                        "Registration was successful, but can't find authentication data in server's response"
                    );
                }
                return {
                    authenticationToken: authData.authentication_token,
                    tokenTTLSeconds: authData.token_ttl_sec
                };
            },
            transformErrorResponse: (response): ErrorResponse => {
                return response.data.response.errors;
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
            async onQueryStarted(_, { dispatch }) {
                dispatch(AuthenticationActions.logout);
            }
        }),
        registrationStatus: builder.query({
            query: () => ({
                url: BackendEndpoints.REGISTRATION_STATUS,
                method: HTTP_METHODS.GET,
                headers: {
                    'Content-Type': 'application/json'
                }
            }),
            transformResponse: (response): RegistrationStatusResponse => {
                return { registrationNeeded: response.needs_registration };
            }
        })
    })
});

export const {
    useLoginMutation,
    useRegisterMutation,
    useLogoutMutation,
    useRegistrationStatusQuery
} = authenticationEndpoints;
