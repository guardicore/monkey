import {
    BaseQueryApi,
    BaseQueryFn,
    createApi,
    fetchBaseQuery
} from '@reduxjs/toolkit/query/react';
import {
    AUTHENTICATION_TOKEN_HEADER,
    AUTHORIZATION_HEADER,
    DEFAULT_QUERY_TIMEOUT
} from '@/redux/features/api/authentication/constants/auth.constants';
import { getApiPath } from '@/constants/paths.constants';
import { getToken } from '@/_lib/authentication';

const baseQuery: BaseQueryFn = fetchBaseQuery({
    baseUrl: getApiPath(),
    prepareHeaders: async (headers: any) => {
        const token = getToken();
        if (token) {
            headers.set(AUTHORIZATION_HEADER, `Bearer ${token}`);
            headers.set(AUTHENTICATION_TOKEN_HEADER, token);
        }
        return headers;
    },
    timeout: DEFAULT_QUERY_TIMEOUT
});

const getIslandBaseQuery = async (
    args: any,
    api: BaseQueryApi,
    extraOptions: object
): Promise<any> => {
    return baseQuery(args, api, extraOptions);
};

export const islandApiSlice = createApi({
    reducerPath: 'islandApi',
    baseQuery: getIslandBaseQuery,
    endpoints: () => ({})
});
