import React, {createContext, useState} from 'react';
import AuthComponent from '../../AuthComponent';

export const PluginsContext = createContext({});

const authComponent = new AuthComponent({});

export const PluginState = () => {

  const [availablePlugins, setAvailablePlugins] = useState([]);
  const [installedPlugins, setInstalledPlugins] = useState([]);
  const [numberOfPluginsThatRequiresUpdate, setNumberOfPluginsThatRequiresUpdate] = useState(0);

  const refreshAvailablePlugins = (forceRefresh = false) => {
    let url = '/api/agent-plugins/available/index';
    if (forceRefresh) {
      url += '?force_refresh=true';
    }
    authComponent.authFetch(url, {}, true)
      .then(res => res.json())
      .then(plugins => {
        setAvailablePlugins(plugins?.plugins || []);
      });
  };

  const refreshInstalledPlugins = () => {
    authComponent.authFetch('/api/agent-plugins/installed/manifests', {}, true)
      .then(res => res.json())
      .then(plugins => {
        setInstalledPlugins(plugins);
      });
  };

  return {
    availablePlugins,
    installedPlugins,
    numberOfPluginsThatRequiresUpdate,
    setAvailablePlugins,
    setInstalledPlugins,
    refreshAvailablePlugins,
    refreshInstalledPlugins
  }
}
