import { GridActionsCellItem } from '@mui/x-data-grid';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import React from 'react';
import { useInstallPluginMutation } from '@/redux/features/api/agentPlugins/agentPluginEndpoints';
import MonkeyLoadingIcon from '@/_components/icons/MonkeyLoadingIcon';
import DownloadDoneIcon from '@mui/icons-material/DownloadDone';

type PluginInstallationButtonProps = {
    pluginType: string;
    pluginName: string;
    pluginVersion: string;
    pluginId: string;
};

const PluginInstallationButton = (props: PluginInstallationButtonProps) => {
    const { pluginType, pluginName, pluginVersion, pluginId } = props;

    const [installPlugin, installationResult] = useInstallPluginMutation({
        fixedCacheKey: pluginId
    });

    const onInstallClick = () => {
        installPlugin({
            pluginVersion: pluginVersion,
            pluginName: pluginName,
            pluginType: pluginType,
            pluginId: pluginId
        });
    };

    if (installationResult.isLoading) {
        return InstallationInProgressButton(pluginId);
    } else if (installationResult.isSuccess) {
        return DownloadDoneButton(pluginId);
    } else {
        return InstallationReadyButton(pluginId, onInstallClick);
    }
};

const InstallationReadyButton = (
    pluginId: string,
    onInstallClick: () => void
) => {
    return (
        <GridActionsCellItem
            key={pluginId}
            icon={<FileDownloadIcon />}
            label="Download"
            className="textPrimary"
            onClick={onInstallClick}
            color="inherit"
        />
    );
};

const InstallationInProgressButton = (pluginId: string) => {
    return (
        <GridActionsCellItem
            key={pluginId}
            icon={<MonkeyLoadingIcon />}
            label="Downloading"
            className="textPrimary"
            color="inherit"
        />
    );
};

const DownloadDoneButton = (pluginId: string) => {
    return (
        <GridActionsCellItem
            key={pluginId}
            icon={<DownloadDoneIcon />}
            label="Download Done"
            className="textPrimary"
            color="inherit"
        />
    );
};

export default PluginInstallationButton;
