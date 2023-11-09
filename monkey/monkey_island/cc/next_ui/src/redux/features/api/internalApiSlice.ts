import {
    BaseQueryApi,
    BaseQueryFn,
    createApi,
    fetchBaseQuery
} from '@reduxjs/toolkit/query/react';
import { DEFAULT_QUERY_TIMEOUT } from '@/redux/features/api/authentication/constants/auth.constants';

const internalBaseQuery: BaseQueryFn = fetchBaseQuery({
    baseUrl: process.env.NEXT_PUBLIC_API_ROUTES_URL,
    credentials: 'include', // send cookies
    timeout: DEFAULT_QUERY_TIMEOUT
});

const getInternalBaseQuery = async (
    args: any,
    api: BaseQueryApi,
    extraOptions: object
): Promise<any> => {
    return await internalBaseQuery(args, api, extraOptions);
};

export const internalApiSlice = createApi({
    reducerPath: 'internalApi',
    baseQuery: getInternalBaseQuery,
    endpoints: () => ({})
});
