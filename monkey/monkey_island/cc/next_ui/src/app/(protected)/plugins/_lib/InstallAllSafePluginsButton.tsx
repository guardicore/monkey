import React from 'react';
import MonkeyButton, {
    ButtonVariant
} from '@/_components/buttons/MonkeyButton';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import {
    useGetAvailablePluginsQuery,
    useGetInstalledPluginsQuery,
    useInstallPluginMutation
} from '@/redux/features/api/agentPlugins/agentPluginEndpoints';
import { filterOutInstalledPlugins } from '@/app/(protected)/plugins/_lib/filters/InstalledPluginFilter';
import { filterOutDangerousPlugins } from '@/app/(protected)/plugins/_lib/filters/SafetyFilter';

const InstallAllSafePluginsButton = () => {
    const { data: availablePlugins, isLoading: isLoadingAvailablePlugins } =
        useGetAvailablePluginsQuery();
    const { data: installedPlugins, isLoading: isLoadingInstalledPlugins } =
        useGetInstalledPluginsQuery();
    const [installPlugin] = useInstallPluginMutation();

    const installAllSafePlugins = () => {
        if (availablePlugins === undefined || installedPlugins === undefined)
            throw new Error('Available or installed plugins are undefined');
        const installablePlugins = filterOutInstalledPlugins(
            availablePlugins,
            installedPlugins
        );
        const safePlugins = filterOutDangerousPlugins(installablePlugins);
        safePlugins.forEach((plugin) => {
            installPlugin({
                pluginVersion: plugin.version,
                pluginName: plugin.name,
                pluginType: plugin.pluginType
            });
        });
    };

    const isDisabled =
        isLoadingAvailablePlugins ||
        isLoadingInstalledPlugins ||
        !availablePlugins;

    return (
        <MonkeyButton
            variant={ButtonVariant.Contained}
            disabled={isDisabled}
            onClick={installAllSafePlugins}>
            <FileDownloadIcon sx={{ mr: '5px' }} />
            All Safe Plugins
        </MonkeyButton>
    );
};

export default InstallAllSafePluginsButton;
