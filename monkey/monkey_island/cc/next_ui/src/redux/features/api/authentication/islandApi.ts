import { HTTP_METHODS } from '@/constants/http.constants';
import { islandApiSlice } from '@/redux/features/api/islandApiSlice';
import { LoginParams } from '@/redux/features/api/types/islandApi';
import handleAuthToken from '@/app/(auth)/_lib/handleAuthToken';

export enum IslandEndpoints {
    LOGIN = '/login',
    MACHINES = '/machines',
    REGISTER = '/register'
}

function provideUnauthorizedTag(result, error) {
    return result
        ? []
        : error?.status === 401
          ? ['UNAUTHORIZED']
          : ['UNKNOWN_ERROR'];
}

export const islandApi = islandApiSlice.injectEndpoints({
    endpoints: (builder: any) => ({
        getAllMachines: builder.query({
            query: () => ({
                url: IslandEndpoints.MACHINES,
                method: HTTP_METHODS.GET
            }),
            providesTags: (result, error, _) =>
                provideUnauthorizedTag(result, error)
        }),
        login: builder.mutation({
            query: (loginValues: LoginParams) => ({
                url: IslandEndpoints.LOGIN,
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
                url: IslandEndpoints.REGISTER,
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

export const { useGetAllMachinesQuery, useLoginMutation, useRegisterMutation } =
    islandApi;
