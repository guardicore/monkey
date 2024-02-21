import {
    AvailablePlugin,
    InstalledPlugin,
    PluginManifestResponse,
    PluginMetadata,
    PluginMetadataResponse
} from '@/redux/features/api/agentPlugins/types';

export const generatePluginId = (
    name: string,
    pluginType: string,
    version: string
): string => {
    return `${name}-${pluginType}-${version}`;
};

export const parsePluginMetadataResponse = (
    response: PluginMetadataResponse
): AvailablePlugin[] => {
    const plugins: AvailablePlugin[] = [];
    for (const pluginType in response) {
        for (const pluginName in response[pluginType]) {
            const unparsedPlugin =
                response[pluginType][pluginName].slice(-1)[0];
            const availablePlugin = parsePluginFromResponse(unparsedPlugin);
            plugins.push(availablePlugin);
        }
    }
    return plugins;
};

const parsePluginFromResponse = (
    unparsedPlugin: PluginMetadata
): AvailablePlugin => {
    return {
        id: generatePluginId(
            unparsedPlugin.name,
            unparsedPlugin.plugin_type,
            unparsedPlugin.version
        ),
        name: unparsedPlugin.name,
        pluginType: unparsedPlugin.plugin_type,
        description: unparsedPlugin.description,
        safe: unparsedPlugin.safe,
        version: unparsedPlugin.version,
        resourcePath: unparsedPlugin.resource_path,
        sha256: unparsedPlugin.sha256
    };
};

export const parsePluginManifestResponse = (
    response: PluginManifestResponse
): InstalledPlugin[] => {
    const plugins: InstalledPlugin[] = [];
    for (const pluginType in response) {
        for (const pluginName in response[pluginType]) {
            const installedVersion =
                response[pluginType][pluginName]['version'];
            const unparsedPlugin = response[pluginType][pluginName];
            const installedPlugin: InstalledPlugin = {
                id: generatePluginId(pluginName, pluginType, installedVersion),
                name: pluginName,
                pluginType: pluginType,
                description: unparsedPlugin['description'],
                safe: unparsedPlugin['safe'],
                version: installedVersion,
                title: unparsedPlugin['title'],
                supportedOperatingSystems:
                    unparsedPlugin['supported_operating_systems'],
                targetOperatingSystems:
                    unparsedPlugin['target_operating_systems'],
                linkToDocumentation: unparsedPlugin['link_to_documentation'],
                remediationSuggestion: unparsedPlugin['remediation_suggestion']
            };
            plugins.push(installedPlugin);
        }
    }
    return plugins;
};
