import React from 'react';
import MonkeyButton, {
    ButtonVariant
} from '@/_components/buttons/MonkeyButton';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import { useGetAvailablePluginsQuery } from '@/redux/features/api/agentPlugins/agentPluginEndpoints';

type InstallAllSafePluginsButtonProps = {};

const InstallAllSafePluginsButton = (
    props: InstallAllSafePluginsButtonProps
) => {
    const { data: availablePlugins, isLoading: isLoadingAvailablePlugins } =
        useGetAvailablePluginsQuery();

    const isDisabled = isLoadingAvailablePlugins || !availablePlugins;
    return (
        <MonkeyButton variant={ButtonVariant.Contained} disabled={isDisabled}>
            <FileDownloadIcon sx={{ mr: '5px' }} />
            All Safe Plugins
        </MonkeyButton>
    );
};

export default InstallAllSafePluginsButton;
