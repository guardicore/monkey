import { PluginRow } from '@/app/(protected)/plugins/_lib/PluginTable';
import { useGetInstalledPluginsQuery } from '@/redux/features/api/agentPlugins/agentPluginEndpoints';
import { FilterProps } from '@/app/(protected)/plugins/available/AvailablePluginFilters';
import { useEffect } from 'react';
import {
    AgentPlugin,
    InstalledPlugin
} from '@/redux/features/api/agentPlugins/types';

type InstalledPluginFilterProps = FilterProps;

export const filterOutInstalledPlugins = (
    plugins: AgentPlugin[],
    installedPlugins: InstalledPlugin[]
) => {
    return plugins.filter((plugin) => {
        return !installedPlugins.find((installedPlugin) => {
            return installedPlugin.id === plugin.id;
        });
    });
};

const InstalledPluginFilter = (props: InstalledPluginFilterProps) => {
    const { setFilterCallback } = props;
    const { data: installedPlugins } = useGetInstalledPluginsQuery();

    const filter = (pluginRow: PluginRow): boolean => {
        if (!installedPlugins) return true;
        const installablePlugin = filterOutInstalledPlugins(
            [pluginRow],
            installedPlugins
        );
        return installablePlugin.length > 0;
    };

    useEffect(() => {
        setFilterCallback('installed', filter);
    }, [installedPlugins]);

    return null;
};

export default InstalledPluginFilter;
