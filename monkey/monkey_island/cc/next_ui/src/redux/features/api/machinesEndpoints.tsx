import { HTTP_METHODS } from '@/constants/http.constants';
import { EndpointBuilder } from '@reduxjs/toolkit/dist/query/endpointDefinitions';
import { islandApiSlice } from '@/redux/features/api/islandApiSlice';

enum BackendEndpoints {
    MACHINES = '/machines'
}

export const machineEndpoints = islandApiSlice.injectEndpoints({
    endpoints: (builder: EndpointBuilder<any, any, any>) => ({
        getAllMachines: builder.query<void, void>({
            query: () => ({
                url: BackendEndpoints.MACHINES,
                method: HTTP_METHODS.GET
            })
        })
    })
});

export const { useGetAllMachinesQuery } = machineEndpoints;
