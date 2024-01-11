import { HTTP_METHODS } from '@/constants/http.constants';
import { islandApiSlice } from '@/redux/features/api/islandApiSlice';
import { LoginParams } from '@/redux/features/api/types/islandApi';
import handleAuthToken from '@/app/(auth)/_lib/handleAuthToken';

enum BackendEndpoints {
    LOGIN = '/login',
    REGISTER = '/register'
}

export const authenticationEndpoints = islandApiSlice.injectEndpoints({
    endpoints: (builder: any) => ({
        login: builder.mutation({
            query: (loginValues: LoginParams) => ({
                url: BackendEndpoints.LOGIN,
                method: HTTP_METHODS.POST,
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(loginValues)
            }),
            // on successful login, will refetch all currently
            // 'UNAUTHORIZED' queries
            invalidatesTags: (result) => (result ? ['UNAUTHORIZED'] : []),
            async onQueryStarted(_, { queryFulfilled }) {
                const { data } = await queryFulfilled;
                handleAuthToken(data);
            }
        }),
        register: builder.mutation({
            query: (loginValues) => ({
                url: BackendEndpoints.REGISTER,
                method: HTTP_METHODS.POST,
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(loginValues)
            }),
            // on successful login, will refetch all currently
            // 'UNAUTHORIZED' queries
            invalidatesTags: (result) => (result ? ['UNAUTHORIZED'] : []),
            async onQueryStarted(_, { queryFulfilled }) {
                const response = await queryFulfilled;
                handleAuthToken(response);
            }
        })
    })
});

export const { useLoginMutation, useRegisterMutation } =
    authenticationEndpoints;
