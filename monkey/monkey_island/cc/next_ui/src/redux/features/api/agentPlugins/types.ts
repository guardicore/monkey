export type AgentPlugin = {
    id: string;
    name: string;
    pluginType: string;
    description: string;
    safe: boolean;
    version: string;
};

export type InstalledPlugin = AgentPlugin & {
    title: string;
    supportedOperatingSystems: string[];
    targetOperatingSystems: string[];
    linkToDocumentation?: string;
    remediationSuggestion?: string;
};

export type AvailablePlugin = AgentPlugin & {
    resourcePath: string;
    sha256: string;
};

export type PluginFromManifest = {
    name: string;
    plugin_type: string;
    supported_operating_systems: string[];
    target_operating_systems: string[];
    title: string;
    version: string;
    description: string;
    remediation_suggestion?: string;
    link_to_documentation?: string;
    safe: boolean;
};

export type PluginManifestResponse = {
    [key: string]: { [key: string]: PluginFromManifest[] };
};

export type PluginMetadata = {
    name: string;
    plugin_type: string;
    resource_path: string;
    sha256: string;
    description: string;
    version: string;
    safe: boolean;
};

export type PluginMetadataResponse = {
    [key: string]: { [key: string]: PluginMetadata[] };
};

export type PluginInfo = {
    pluginType: string;
    pluginName: string;
    pluginVersion: string;
    pluginId: string;
};
