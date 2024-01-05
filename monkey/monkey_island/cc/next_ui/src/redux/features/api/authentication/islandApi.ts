import { HTTP_METHODS } from '@/constants/http.constants';
import { islandApiSlice } from '@/redux/features/api/islandApiSlice';

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
        })
    })
});

export const { useGetAllMachinesQuery } = islandApi;
