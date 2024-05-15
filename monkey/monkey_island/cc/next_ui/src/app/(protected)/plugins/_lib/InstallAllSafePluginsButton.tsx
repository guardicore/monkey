import React, { useState } from 'react';
import MonkeyButton, {
    ButtonVariant
} from '@/_components/buttons/MonkeyButton';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import { agentPluginEndpoints } from '@/redux/features/api/agentPlugins/agentPluginEndpoints';
import { filterOutDangerousPlugins } from '@/app/(protected)/plugins/_lib/filters/SafetyFilter';
import MonkeyLoadingIcon from '@/_components/icons/MonkeyLoadingIcon';
import { useDispatch } from 'react-redux';
import useInstallablePlugins from '@/app/(protected)/plugins/_lib/useInstallablePlugins';

const InstallAllSafePluginsButton = () => {
    const [loading, setLoading] = useState(false);
    const dispatch = useDispatch();
    const installablePlugins = useInstallablePlugins();
    const installableSafePlugins =
        installablePlugins === undefined
            ? []
            : filterOutDangerousPlugins(installablePlugins);

    const installAllSafePlugins = async () => {
        setLoading(true);

        const installationPromises = [];
        installableSafePlugins.forEach((plugin) => {
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

    const isDisabled = installableSafePlugins.length === 0;

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
