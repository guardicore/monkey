import { HTTP_METHODS } from '@/constants/http.constants';
import { EndpointBuilder } from '@reduxjs/toolkit/dist/query/endpointDefinitions';
import { islandApiSlice } from '@/redux/features/api/islandApiSlice';
import {
    AvailablePlugin,
    InstalledPlugin,
    PluginManifestResponse,
    PluginMetadataResponse
} from '@/redux/features/api/agentPlugins/types';
import {
    parsePluginManifestResponse,
    parsePluginMetadataResponse
} from '@/redux/features/api/agentPlugins/responseParsers';

enum BackendEndpoints {
    PLUGIN_INDEX = '/agent-plugins/available/index',
    PLUGIN_INDEX_FORCE_REFRESH = `${BackendEndpoints.PLUGIN_INDEX}?force_refresh=true`,
    PLUGIN_INSTALL = '/install-agent-plugin',
    PLUGIN_MANIFESTS = '/agent-plugins/installed/manifests'
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
                return parsePluginMetadataResponse(response.plugins);
            }
        }),
        getInstalledPlugins: builder.query<InstalledPlugin[], void>({
            query: () => ({
                url: BackendEndpoints.PLUGIN_MANIFESTS,
                method: HTTP_METHODS.GET
            }),
            transformResponse: (
                response: PluginManifestResponse
            ): InstalledPlugin[] => {
                return parsePluginManifestResponse(response);
            }
        })
    })
});

export const { useGetAvailablePluginsQuery, useGetInstalledPluginsQuery } =
    agentPluginEndpoints;
