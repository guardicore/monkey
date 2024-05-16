import { GridActionsCellItem } from '@mui/x-data-grid';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import React from 'react';
import {
    useGetLatestPluginVersionQuery,
    useInstallPluginMutation
} from '@/redux/features/api/agentPlugins/agentPluginEndpoints';
import MonkeyLoadingIcon from '@/_components/icons/MonkeyLoadingIcon';
import DownloadDoneIcon from '@mui/icons-material/DownloadDone';
import { PluginId, PluginInfo } from '@/redux/features/api/agentPlugins/types';

const PluginUpgradeButton = (props: PluginInfo) => {
    const { pluginType, pluginName, pluginVersion, pluginId } = props;

    const [
        upgradePlugin,
        {
            isLoading: isUpgrading,
            isSuccess: isUpgradeSuccessful,
            reset: resetUpgradePlugin
        }
    ] = useInstallPluginMutation({ fixedCacheKey: pluginName + pluginType });
    const { data: latestPluginVersion, isLoading: isLoadingLatestVersion } =
        useGetLatestPluginVersionQuery({
            pluginType: pluginType,
            pluginName: pluginName
        });

    const isUpgradable = React.useMemo(() => {
        if (!latestPluginVersion) {
            return false;
        }
        const upgradeAvailable = latestPluginVersion !== pluginVersion;
        upgradeAvailable && isUpgradeSuccessful && resetUpgradePlugin();
        return upgradeAvailable;
    }, [latestPluginVersion, pluginVersion]);

    const onUpgradeClick = () => {
        upgradePlugin({
            pluginVersion: String(latestPluginVersion),
            pluginName: pluginName,
            pluginType: pluginType,
            pluginId: pluginId
        });
    };

    if (isUpgrading) {
        return UpgradeInProgressButton(pluginId);
    } else if (isUpgradeSuccessful) {
        return UpgradeDoneButton(pluginId);
    } else if (isLoadingLatestVersion || !isUpgradable) {
        return;
    } else {
        return UpgradeButton(pluginId, onUpgradeClick);
    }
};

const UpgradeButton = (pluginId: PluginId, onUpgradeClick: () => void) => {
    return (
        <GridActionsCellItem
            key={pluginId}
            icon={<FileDownloadIcon />}
            label="Download"
            onClick={onUpgradeClick}
        />
    );
};

const UpgradeInProgressButton = (pluginId: PluginId) => {
    return (
        <GridActionsCellItem
            key={pluginId}
            icon={<MonkeyLoadingIcon />}
            label="Upgrading"
        />
    );
};

const UpgradeDoneButton = (pluginId: PluginId) => {
    return (
        <GridActionsCellItem
            key={pluginId}
            icon={<DownloadDoneIcon />}
            label="Upgrade Complete"
        />
    );
};

export default PluginUpgradeButton;
