import { HTTP_METHODS } from '@/constants/http.constants';
import { islandApiSlice } from '@/redux/features/api/islandApiSlice';

enum BackendEndpoints {
    MACHINES = '/machines'
}

function provideUnauthorizedTag(result, error) {
    return result
        ? []
        : error?.status === 401
          ? ['UNAUTHORIZED']
          : ['UNKNOWN_ERROR'];
}

export const machineEndpoints = islandApiSlice.injectEndpoints({
    endpoints: (builder: any) => ({
        getAllMachines: builder.query({
            query: () => ({
                url: BackendEndpoints.MACHINES,
                method: HTTP_METHODS.GET
            }),
            providesTags: (result, error) =>
                provideUnauthorizedTag(result, error)
        })
    })
});

export const { useGetAllMachinesQuery } = machineEndpoints;
