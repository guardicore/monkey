import {
    BaseQueryApi,
    BaseQueryFn,
    createApi,
    fetchBaseQuery
} from '@reduxjs/toolkit/query/react';
import { getSession } from 'next-auth/react';
import {
    ACCESS_TOKEN,
    AUTHENTICATION_TOKEN_HEADER,
    AUTHORIZATION_HEADER,
    DEFAULT_QUERY_TIMEOUT
} from '@/redux/features/api/authentication/constants/auth.constants';

// fetchBaseQuery is using GET method by default
// pass (args, api, extraOptions) as params to the baseQuery function if needed, e.g.:
// const baseQuery: BaseQueryFn = (args, api, extraOptions) => {return fetchBaseQuery({})};
const baseQuery: BaseQueryFn = fetchBaseQuery({
    baseUrl: process.env.NEXT_PUBLIC_EXTERNAL_API_BASE_URL,
    prepareHeaders: async (headers: any) => {
        const session: any = await getSession();
        if (session) {
            if (session[ACCESS_TOKEN]) {
                headers.set(
                    AUTHORIZATION_HEADER,
                    `Bearer ${session.accessToken}`
                );
                headers.set(AUTHENTICATION_TOKEN_HEADER, session.accessToken);
            }
        }
        return headers;
    },
    timeout: DEFAULT_QUERY_TIMEOUT
});

const getExternalBaseQuery = async (
    args: any,
    api: BaseQueryApi,
    extraOptions: object
): Promise<any> => {
    return await baseQuery(args, api, extraOptions);
};

export const externalApiSlice = createApi({
    reducerPath: 'externalApi',
    baseQuery: getExternalBaseQuery,
    endpoints: () => ({})
});
