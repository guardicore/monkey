import {
    AgentPlugin,
    InstalledPlugin
} from '@/redux/features/api/agentPlugins/types';

export const filterOutInstalledPlugins = (
    plugins: AgentPlugin[],
    installedPlugins: InstalledPlugin[]
) => {
    return plugins.filter((plugin) => {
        return !installedPlugins.find((installedPlugin) => {
            return (
                installedPlugin.name === plugin.name &&
                installedPlugin.pluginType === plugin.pluginType
            );
        });
    });
};
