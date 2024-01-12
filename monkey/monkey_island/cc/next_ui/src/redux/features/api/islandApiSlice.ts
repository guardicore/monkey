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
import {
    AgentConfiguration,
    RegistrationStatus
} from '@/redux/features/api/types/islandApi';
import transformSchema from '@/app/(protected)/configuration/transform_schema';

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

function provideUnauthorizedTag(result, error) {
    return result
        ? []
        : error?.status === 401
          ? ['UNAUTHORIZED']
          : ['UNKNOWN_ERROR'];
}

// API:
// - Agent Binary
//   - GET, PUT /api/agent-binaries/:os/masque
//   - GET /api/agent-binaries/:os
// - Agent Configuration
//   - GET /api/agent-configuration-schema
//   - GET, PUT /api/agent-configuration
//   - POST /api/reset-agent-configuration
// - Agent Plugins
//   - (GET) /api/agent-plugins/:plugin_type/:name/manifest
//   - (GET) /api/agent-plugins/:host_os/:plugin_type/:name
//   - GET /api/agent-plugins/available/index
//   - PUT /api/install-agent-plugin
//   - GET /api/agent-plugins/installed/manifests
//   - POST /api/uninstall-agent-plugin
// - Agent Signals
//   - (GET) /api/agent-signals/:agentId
//   - POST /api/agent-signals/terminate-all-agents
// - Exploitations
//   - GET /api/exploitations/monkey
// - GET, (POST) /api/agent-events
// - (POST) /api/agent/:agentId/heartbeat
// - GET, (POST) /api/agents
// - POST /api/clear-simulation-data
// - GET /api/machines
// - GET /api/nodes
// - GET /api/propagation-credentials
// - GET, PUT /api/propagation-credentials/:collection
// - GET /api
// - Logs
//   - GET, (PUT) /api/agent-logs/:agent_id
//   - GET /api/island/log
// - Report
//   - GET /api/security-report
//   - GET /api/report/ransomware
//   - GET /api/report-generation-status
// - Run
//   - POST /api/local-monkey
//   - GET, POST /api/remote-monkey
// - GET /api/island/version
export const islandApiSlice = createApi({
    reducerPath: 'islandApi',
    baseQuery: getIslandBaseQuery,
    endpoints: (builder) => ({
        getNeedsRegistration: builder.query<RegistrationStatus, void>({
            query: () => `/registration-status`
        }),
        getAgentConfiguration: builder.query<AgentConfiguration, void>({
            query: () => `/agent-configuration`,
            providesTags: (result, error, id) =>
                provideUnauthorizedTag(result, error)
        }),
        putAgentConfiguration: builder.mutation<
            AgentConfiguration,
            AgentConfiguration
        >({
            query: (data) => ({
                url: `/agent-configuration`,
                method: 'PUT',
                body: data
            })
        }),
        postResetAgentConfiguration: builder.mutation<void, void>({
            query: () => ({
                url: `/reset-agent-configuration`,
                method: 'POST'
            })
        }),
        getAgentConfigurationSchema: builder.query<AgentConfiguration, void>({
            query: () => `/agent-configuration-schema`,
            providesTags: (result, error, id) =>
                provideUnauthorizedTag(result, error),
            transformResponse: async (response: any) => {
                return await transformSchema(response);
            }
        }),
        getAgentBinaryMasque: builder.query<Blob, string>({
            query: (os) => `/agent-binaries/${os}/masque`
        }),
        putAgentBinaryMasque: builder.mutation<
            Blob,
            { os: string; data: Blob }
        >({
            query: ({ os, data }) => ({
                url: `/agent-binaries/${os}/masque`,
                method: 'PUT',
                body: data
            })
        }),
        getPropagationCredentials: builder.query<any, string>({
            query: (collection) => `/propagation-credentials/${collection}`
        }),
        putPropagationCredentials: builder.mutation<
            any,
            { collection: string; data: any }
        >({
            query: ({ collection, data }) => ({
                url: `/propagation-credentials/${collection}`,
                method: 'PUT',
                body: data
            })
        })
    })
});

export const {
    useGetNeedsRegistrationQuery,
    useGetAgentConfigurationQuery,
    usePutAgentConfigurationMutation,
    usePostResetAgentConfigurationMutation,
    useGetAgentConfigurationSchemaQuery,
    useGetAgentBinaryMasqueQuery,
    usePutAgentBinaryMasqueMutation,
    useGetPropagationCredentialsQuery,
    usePutPropagationCredentialsMutation
} = islandApiSlice;
