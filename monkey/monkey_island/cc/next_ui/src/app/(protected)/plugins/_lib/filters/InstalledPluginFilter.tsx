import { PluginRow } from '@/app/(protected)/plugins/_lib/PluginTable';
import { useGetInstalledPluginsQuery } from '@/redux/features/api/agentPlugins/agentPluginEndpoints';
import { FilterProps } from '@/app/(protected)/plugins/available/AvailablePluginFilters';
import { useEffect } from 'react';

type InstalledPluginFilterProps = FilterProps;

const InstalledPluginFilter = (props: InstalledPluginFilterProps) => {
    const { data: installedPlugins } = useGetInstalledPluginsQuery();
    const filter = (pluginRow: PluginRow): boolean => {
        if (!installedPlugins) return true;
        const installedPlugin = installedPlugins.find(
            (installedPlugin) => pluginRow.id === installedPlugin.id
        );
        return !installedPlugin;
    };
    useEffect(() => {
        props.setFiltersCallback({ installed: filter });
    }, [installedPlugins]);

    return null;
};

export default InstalledPluginFilter;
