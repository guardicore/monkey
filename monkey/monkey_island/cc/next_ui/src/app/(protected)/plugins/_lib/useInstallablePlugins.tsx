import {
    useGetAvailablePluginsQuery,
    useGetInstalledPluginsQuery
} from '@/redux/features/api/agentPlugins/agentPluginEndpoints';
import { filterOutInstalledPlugins } from '@/app/(protected)/plugins/_lib/filters/InstalledPluginFilter';
import { useMemo } from 'react';

function useInstallablePlugins() {
    const { data: availablePlugins } = useGetAvailablePluginsQuery();
    const { data: installedPlugins } = useGetInstalledPluginsQuery();

    return useMemo(() => {
        if (availablePlugins === undefined || installedPlugins === undefined) {
            return;
        }
        return filterOutInstalledPlugins(availablePlugins, installedPlugins);
    }, [availablePlugins, installedPlugins]);
}

export default useInstallablePlugins;
