import React from 'react';
import MonkeyButton, {
    ButtonVariant
} from '@/_components/buttons/MonkeyButton';
import FileDownloadIcon from '@mui/icons-material/FileDownload';

type InstallAllSafePluginsButtonProps = {
    onInstallClick: (
        id: string,
        name: string,
        pluginType: string,
        version: string
    ) => void;
};

const InstallAllSafePluginsButton = (
    props: InstallAllSafePluginsButtonProps
) => {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const { onInstallClick } = props;
    return (
        <MonkeyButton variant={ButtonVariant.Contained}>
            <FileDownloadIcon sx={{ mr: '5px' }} />
            All Safe Plugins
        </MonkeyButton>
    );
};

export default InstallAllSafePluginsButton;
