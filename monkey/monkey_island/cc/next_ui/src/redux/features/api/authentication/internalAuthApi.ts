import { internalApiSlice } from '@/redux/features/api/internalApiSlice';
import { API_AUTH_ENDPOINTS } from '@/redux/features/api/authentication/constants/auth.constants';
import { signOut } from 'next-auth/react';
import { HTTP_METHODS } from '@/constants/http.constants';
import { AUTH_PATHS } from '@/constants/authPaths.constants';

const customExtraOptions = {
    isInternalRequest: true
};

export const internalAuthApi = internalApiSlice.injectEndpoints({
    endpoints: (builder: any) => ({
        register: builder.mutation({
            query: (data: any) => ({
                url: API_AUTH_ENDPOINTS.REGISTER,
                method: HTTP_METHODS.POST,
                body: data
            }),
            async onQueryStarted(
                arg: any,
                { queryFulfilled }: any
            ): Promise<void> {
                try {
                    const { data } = await queryFulfilled;
                    if (data.status === 200) {
                        console.log('Register data here', data);
                    }
                    // @ts-ignore
                } catch ({ error: { data } }) {
                    console.log('Register catch error: ', data);
                }
            }
        }),
        logout: builder.mutation({
            query: () => ({
                url: API_AUTH_ENDPOINTS.LOGOUT,
                method: HTTP_METHODS.POST
            }),
            async onQueryStarted(
                arg: any,
                { queryFulfilled }: any
            ): Promise<void> {
                try {
                    const { data } = await queryFulfilled;

                    if (data) {
                        await signOut({ callbackUrl: AUTH_PATHS.SIGN_IN });
                    }
                } catch (error) {
                    console.log('An error occurred while logging out');
                    console.log(error);
                }
            },
            extraOptions: customExtraOptions
        })
    })
});

export const { useLogoutMutation, useRegisterMutation } = internalAuthApi;
