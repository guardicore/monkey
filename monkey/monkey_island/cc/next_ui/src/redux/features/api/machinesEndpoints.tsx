import { HTTP_METHODS } from '@/constants/http.constants';
import { islandApiSlice } from '@/redux/features/api/islandApiSlice';

enum BackendEndpoints {
    MACHINES = '/machines'
}

export const machineEndpoints = islandApiSlice.injectEndpoints({
    endpoints: (builder: any) => ({
        getAllMachines: builder.query({
            query: () => ({
                url: BackendEndpoints.MACHINES,
                method: HTTP_METHODS.GET
            })
        })
    })
});

export const { useGetAllMachinesQuery } = machineEndpoints;
