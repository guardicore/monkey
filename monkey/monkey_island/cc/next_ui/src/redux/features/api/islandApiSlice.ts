import {
    BaseQueryApi,
    BaseQueryFn,
    createApi,
    fetchBaseQuery
} from '@reduxjs/toolkit/query/react';
import {
    AUTHENTICATION_TOKEN_HEADER,
    DEFAULT_QUERY_TIMEOUT
} from '@/redux/features/api/authentication/authenticationConstants';
import { getApiPath } from '@/constants/paths.constants';
import { getToken, isTokenStored } from '@/_lib/authentication';
import { AuthenticationActions } from '@/redux/features/api/authentication/authenticationActions';

const baseQuery: BaseQueryFn = fetchBaseQuery({
    baseUrl: getApiPath(),
    prepareHeaders: async (headers: any) => {
        const token = getToken();
        if (token) {
            headers.set(AUTHENTICATION_TOKEN_HEADER, token);
        }
        return headers;
    },
    timeout: DEFAULT_QUERY_TIMEOUT
});

const baseQueryWrapper = async (
    args: any,
    api: BaseQueryApi,
    extraOptions: object
): Promise<any> => {
    const result = await baseQuery(args, api, extraOptions);
    if (result.error?.status === 401 && isTokenStored()) {
        api.dispatch(AuthenticationActions.logout);
    }
    return result;
};

const getIslandBaseQuery = async (
    args: any,
    api: BaseQueryApi,
    extraOptions: object
): Promise<any> => {
    return baseQueryWrapper(args, api, extraOptions);
};

export const islandApiSlice = createApi({
    reducerPath: 'islandApi',
    baseQuery: getIslandBaseQuery,
    endpoints: () => ({})
});
