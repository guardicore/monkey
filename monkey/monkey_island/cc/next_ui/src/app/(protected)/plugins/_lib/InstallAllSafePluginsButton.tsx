import React, { useState } from 'react';
import MonkeyButton, {
    ButtonVariant
} from '@/_components/buttons/MonkeyButton';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import {
    agentPluginEndpoints,
    useGetAvailablePluginsQuery,
    useGetInstalledPluginsQuery
} from '@/redux/features/api/agentPlugins/agentPluginEndpoints';
import { filterOutInstalledPlugins } from '@/app/(protected)/plugins/_lib/filters/InstalledPluginFilter';
import { filterOutDangerousPlugins } from '@/app/(protected)/plugins/_lib/filters/SafetyFilter';
import MonkeyLoadingIcon from '@/_components/icons/MonkeyLoadingIcon';
import { useDispatch } from 'react-redux';

const InstallAllSafePluginsButton = () => {
    const { data: availablePlugins, isLoading: isLoadingAvailablePlugins } =
        useGetAvailablePluginsQuery();
    const { data: installedPlugins, isLoading: isLoadingInstalledPlugins } =
        useGetInstalledPluginsQuery();
    const [loading, setLoading] = useState(false);
    const dispatch = useDispatch();

    const installAllSafePlugins = async () => {
        if (availablePlugins === undefined || installedPlugins === undefined)
            throw new Error('Available or installed plugins are undefined');

        setLoading(true);
        const installablePlugins = filterOutInstalledPlugins(
            availablePlugins,
            installedPlugins
        );
        const safePlugins = filterOutDangerousPlugins(installablePlugins);
        const installationPromises = [];
        safePlugins.forEach((plugin) => {
            installationPromises.push(
                // @ts-ignore
                dispatch(
                    // @ts-ignore
                    agentPluginEndpoints.endpoints.installPlugin.initiate(
                        {
                            pluginVersion: plugin.version,
                            pluginName: plugin.name,
                            pluginType: plugin.pluginType,
                            pluginId: plugin.id
                        },
                        { fixedCacheKey: plugin.id }
                    )
                )
            );
        });
        await Promise.all(installationPromises);
        setLoading(false);
    };

    const isDisabled =
        isLoadingAvailablePlugins ||
        isLoadingInstalledPlugins ||
        !availablePlugins;

    const buttonIcon = loading ? (
        <MonkeyLoadingIcon sx={{ mr: '5px' }} />
    ) : (
        <FileDownloadIcon sx={{ mr: '5px' }} />
    );

    return (
        <MonkeyButton
            variant={ButtonVariant.Contained}
            disabled={isDisabled}
            onClick={installAllSafePlugins}>
            {buttonIcon}
            All Safe Plugins
        </MonkeyButton>
    );
};

export default InstallAllSafePluginsButton;
