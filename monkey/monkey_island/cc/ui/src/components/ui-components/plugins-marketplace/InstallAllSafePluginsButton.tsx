import React, {useContext, useEffect, useMemo, useState} from 'react';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import LoadingIcon from '../LoadingIconMUI';
import {PluginsContext} from '../../contexts/plugins/PluginsContext';
import {isPluginInstalled} from './AvailablePlugins';
import MonkeyButton, {ButtonVariant} from '../MonkeyButton';

type InstallAllSafePluginsButtonProps = {
  onInstallClick: (id: string, name: string, pluginType: string, version: string) => void;
  pluginsInInstallationProcess: string[];
}

const InstallAllSafePluginsButton = (props: InstallAllSafePluginsButtonProps) => {
  const {availablePlugins, installedPlugins} = useContext(PluginsContext);
  const [installationInProgress, setInstallationInProgress] = useState(false);

  const uninstalledSafePlugins = useMemo(() => {
    let safePlugins = availablePlugins.filter(plugin => plugin.safe);
    return safePlugins.filter(plugin => {
      return ! isPluginInstalled(plugin, installedPlugins);
    });
  }, [availablePlugins, installedPlugins]);

  const isButtonDisabled = useMemo(() => {
    return uninstalledSafePlugins.length === 0;
  }, [uninstalledSafePlugins]);

  useEffect(() => {
    if (props.pluginsInInstallationProcess.length === 0) {
      setInstallationInProgress(false);
    }
  }, [props.pluginsInInstallationProcess]);

  const installAllSafePlugins = () => {
    setInstallationInProgress(true);
    uninstalledSafePlugins.map(plugin =>
      props.onInstallClick(plugin.id,
                           plugin.name,
                           plugin.pluginType,
                           plugin.version)
    );
  }

  return (
    <MonkeyButton onClick={installAllSafePlugins}
                  disabled={isButtonDisabled}
                  variant={ButtonVariant.Contained}>
      {installationInProgress ? <LoadingIcon/> : <FileDownloadIcon/>} All Safe Plugins
    </MonkeyButton>
  )
}

export default InstallAllSafePluginsButton;
