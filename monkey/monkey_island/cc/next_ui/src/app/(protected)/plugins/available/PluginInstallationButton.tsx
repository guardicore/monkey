import { GridActionsCellItem } from '@mui/x-data-grid';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import React from 'react';
import { useInstallPluginMutation } from '@/redux/features/api/agentPlugins/agentPluginEndpoints';
import LoadingIcon from '@/_components/icons/loading-icon/LoadingIcon';
import DownloadDoneIcon from '@mui/icons-material/DownloadDone';

type PluginInstallationButtonProps = {
    pluginType: string;
    pluginName: string;
    pluginVersion: string;
    pluginId: string;
};

const PluginInstallationButton = (props: PluginInstallationButtonProps) => {
    const { pluginType, pluginName, pluginVersion, pluginId } = props;

    const [installPlugin, installationResult] = useInstallPluginMutation();

    const onInstallClick = (
        pluginName: string,
        pluginType: string,
        pluginVersion: string
    ) => {
        installPlugin({
            pluginVersion: pluginVersion,
            pluginName: pluginName,
            pluginType: pluginType
        });
    };

    if (installationResult.isLoading) {
        return InstallationInProgressButton(pluginId);
    } else if (installationResult.isSuccess) {
        return DownloadDoneButton(pluginId);
    }

    return (
        <GridActionsCellItem
            key={pluginId}
            icon={<FileDownloadIcon />}
            label="Download"
            className="textPrimary"
            onClick={() =>
                onInstallClick(pluginName, pluginType, pluginVersion)
            }
            color="inherit"
        />
    );
};

const InstallationInProgressButton = (pluginId: string) => {
    return (
        <GridActionsCellItem
            key={pluginId}
            icon={<LoadingIcon />}
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
