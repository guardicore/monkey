import {
    BaseQueryApi,
    BaseQueryFn,
    createApi,
    fetchBaseQuery
} from '@reduxjs/toolkit/query/react';
import { getApiPath } from '@/constants/paths.constants';
import { getToken, tokenIsStored } from '@/lib/authenticationToken';
import { AuthenticationActions } from '@/redux/features/api/authentication/authenticationActions';

export const DEFAULT_QUERY_TIMEOUT: number = 10000;
export const AUTHENTICATION_TOKEN_HEADER: string = 'authentication-token';

const baseQuery: BaseQueryFn = fetchBaseQuery({
    baseUrl: getApiPath(),
    prepareHeaders: async (headers: any) => {
        const token = getToken();
        if (token) {
            headers.set(AUTHENTICATION_TOKEN_HEADER, token);
        }
        headers.set('Content-Type', 'application/json');
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
    // @ts-ignore
    if (result.error?.status === 401 && tokenIsStored()) {
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
