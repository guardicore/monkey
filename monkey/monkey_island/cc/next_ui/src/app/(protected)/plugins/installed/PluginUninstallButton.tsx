import { GridActionsCellItem } from '@mui/x-data-grid';
import React from 'react';
import {
    useInstallPluginMutation,
    useUninstallPluginMutation
} from '@/redux/features/api/agentPlugins/agentPluginEndpoints';
import MonkeyLoadingIcon from '@/_components/icons/MonkeyLoadingIcon';
import { PluginId, PluginInfo } from '@/redux/features/api/agentPlugins/types';
import DeleteIcon from '@mui/icons-material/Delete';

const PluginUninstallButton = (props: PluginInfo) => {
    const [uninstallPlugin, { isLoading: isUninstalling }] =
        useUninstallPluginMutation();
    const { reset } = useInstallPluginMutation({
        fixedCacheKey: props.pluginName + props.pluginType
    })[1];

    const onUninstallClick = () => {
        uninstallPlugin(props).then(() => reset());
    };

    const UninstallButton = () => {
        return (
            <GridActionsCellItem
                key={props.pluginId + 'uninstall'}
                icon={<DeleteIcon />}
                label="Uninstall"
                onClick={() => onUninstallClick()}
            />
        );
    };

    if (isUninstalling) {
        return UninstallInProgressButton(props.pluginId);
    } else {
        return UninstallButton();
    }
};

const UninstallInProgressButton = (pluginId: PluginId) => {
    return (
        <GridActionsCellItem
            key={pluginId}
            icon={<MonkeyLoadingIcon />}
            label="Uninstalling"
        />
    );
};

export default PluginUninstallButton;
