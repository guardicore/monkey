import { API_AUTH_ENDPOINTS } from '@/redux/features/api/authentication/constants/auth.constants';
import { signOut } from 'next-auth/react';
import { HTTP_METHODS } from '@/constants/http.constants';
import { islandApiSlice } from '@/redux/features/api/islandApiSlice';

const customExtraOptions = {
    isInternalRequest: true
};

export enum IslandEndpoints {
    MACHINES = '/machines'
}

export const islandApi = islandApiSlice.injectEndpoints({
    endpoints: (builder: any) => ({
        getAllMachines: builder.query({
            query: () => ({
                url: IslandEndpoints.MACHINES,
                method: HTTP_METHODS.GET
            })
        }),
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
                        await signOut({ redirect: false });
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

export const {
    useGetAllMachinesQuery,
    useRegisterMutation,
    useLogoutMutation
} = islandApi;
