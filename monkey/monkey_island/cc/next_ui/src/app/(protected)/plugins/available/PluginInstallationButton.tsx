import { GridActionsCellItem } from '@mui/x-data-grid';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import React from 'react';
import { useInstallPluginMutation } from '@/redux/features/api/agentPlugins/agentPluginEndpoints';
import LoadingIcon from '@/_components/icons/loading-icon/LoadingIcon';
import DownloadDoneIcon from '@mui/icons-material/DownloadDone';
import {
    InstallationStatus,
    selectStatusByPluginId
} from '@/redux/features/api/agentPlugins/pluginInstallationStatusSlice';
import { useSelector } from 'react-redux';
import { RootState } from '@/redux/store';

type PluginInstallationButtonProps = {
    pluginType: string;
    pluginName: string;
    pluginVersion: string;
    pluginId: string;
};

const PluginInstallationButton = (props: PluginInstallationButtonProps) => {
    const { pluginType, pluginName, pluginVersion, pluginId } = props;

    const [installPlugin] = useInstallPluginMutation();
    const installationStatus = useSelector((state: RootState) =>
        selectStatusByPluginId(state, pluginId)
    );

    const onInstallClick = () => {
        installPlugin({
            pluginVersion: pluginVersion,
            pluginName: pluginName,
            pluginType: pluginType,
            pluginId: pluginId
        });
    };

    if (installationStatus === InstallationStatus.PENDING) {
        return InstallationInProgressButton(pluginId);
    } else if (installationStatus === InstallationStatus.SUCCESS) {
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
