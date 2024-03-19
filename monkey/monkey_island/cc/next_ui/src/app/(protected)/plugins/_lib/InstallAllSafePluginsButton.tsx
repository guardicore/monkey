import React from 'react';
import MonkeyButton, {
    ButtonVariant
} from '@/_components/buttons/MonkeyButton';

type InstallAllSafePluginsButtonProps = {
    onInstallClick: (
        id: string,
        name: string,
        pluginType: string,
        version: string
    ) => void;
    pluginsInInstallationProcess: string[];
};

const InstallAllSafePluginsButton = (
    props: InstallAllSafePluginsButtonProps
) => {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const { onInstallClick, pluginsInInstallationProcess } = props;
    return (
        <MonkeyButton variant={ButtonVariant.Contained}>
            All Safe Plugins
        </MonkeyButton>
    );
};

export default InstallAllSafePluginsButton;
