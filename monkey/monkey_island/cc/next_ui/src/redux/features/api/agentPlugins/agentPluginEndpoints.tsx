import { HTTP_METHODS } from '@/constants/http.constants';
import { EndpointBuilder } from '@reduxjs/toolkit/dist/query/endpointDefinitions';
import { islandApiSlice } from '@/redux/features/api/islandApiSlice';
import {
    AvailablePlugin,
    PluginMetadataResponse
} from '@/redux/features/api/agentPlugins/types';
import { parsePluginMetadataResponse } from '@/redux/features/api/agentPlugins/responseParsers';

enum BackendEndpoints {
    PLUGIN_INDEX = '/agent-plugins/available/index',
    PLUGIN_INDEX_FORCE_REFRESH = `${BackendEndpoints.PLUGIN_INDEX}?force_refresh=true`,
    PLUGIN_INSTALL = '/api/install-agent-plugin',
    PLUGIN_MANIFESTS = '/api/agent-plugins/installed/manifests'
}

export const agentPluginEndpoints = islandApiSlice.injectEndpoints({
    endpoints: (builder: EndpointBuilder<any, any, any>) => ({
        getAvailablePlugins: builder.query<AvailablePlugin[], void>({
            query: () => ({
                url: BackendEndpoints.PLUGIN_INDEX,
                method: HTTP_METHODS.GET
            }),
            transformResponse: (response: {
                plugins: PluginMetadataResponse;
            }): AvailablePlugin[] => {
                console.log('response', response);
                return parsePluginMetadataResponse(response.plugins);
            }
        })
    })
});

export const { useGetAvailablePluginsQuery } = agentPluginEndpoints;
