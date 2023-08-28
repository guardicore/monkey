import React, {createContext, useEffect, useState} from 'react';
import AuthComponent from '../../AuthComponent';
import semver from 'semver';
import _ from 'lodash';

export const PluginsContext = createContext({});

const authComponent = new AuthComponent({});

export const PluginState = () => {
  const [allPlugins, setAllPlugins] = useState([]);
  const [allInstalledPlugins, setAllInstalledPlugins] = useState([]);
  const [availablePlugins, setAvailablePlugins] = useState([]);
  const [installedPlugins, setInstalledPlugins] = useState([]);
  const [numberOfPluginsThatRequiresUpdate, setNumberOfPluginsThatRequiresUpdate] = useState(0);

  useEffect(() => {
    refreshAllAvailablePlugins();
    refreshInstalledPlugins();
  }, []);

  useEffect(() => {
    refreshAvailablePlugins();
  }, [allPlugins, allInstalledPlugins]);

  useEffect(() => {
    setInstalledPlugins(getInstalledPlugins());
  }, [allPlugins, allInstalledPlugins]);

  useEffect(() => {
    refreshNuberOfUpgradablePlugins();
  }, [installedPlugins]);

  const refreshAllAvailablePlugins = (forceRefresh = false) => {
    let url = '/api/agent-plugins/available/index';
    if (forceRefresh) {
      url += '?force_refresh=true';
    }
    authComponent.authFetch(url, {}, true)
      .then(res => res.json())
      .then(plugins => {
        setAllPlugins(plugins?.plugins || []);
      });
  };

  const refreshAvailablePlugins = (forceRefresh = false) => {
    if (forceRefresh) {
      refreshAllAvailablePlugins(true);
    }
    else {
      setAvailablePlugins(getAvailablePlugins());
    }
  }

  const refreshInstalledPlugins = () => {
    authComponent.authFetch('/api/agent-plugins/installed/manifests', {}, true)
      .then(res => res.json())
      .then(plugins => {
        setAllInstalledPlugins(plugins);
      });
  };

  const refreshNuberOfUpgradablePlugins = () => {
    const numUpgradablePlugins = _.sumBy(installedPlugins, (plugin) => plugin.update_available);
    setNumberOfPluginsThatRequiresUpdate(numUpgradablePlugins);
  }

  const getAvailablePlugins = () => {
    let plugins = [];
    for (const plugin_type in allPlugins) {
      for (const plugin_name in allPlugins[plugin_type]) {
        if (!pluginIsInstalled(plugin_type, plugin_name)) {
          plugins.push(allPlugins[plugin_type][plugin_name].slice(-1)[0]);
        }
      }
    }
    return plugins;
  }

  const pluginIsInstalled = (pluginType, name) => {
    return pluginType in allInstalledPlugins && name in allInstalledPlugins[pluginType];
  }

  const getInstalledPlugins = () => {
    let plugins = [];
    for (const plugin_type in allInstalledPlugins) {
      for (const plugin_name in allInstalledPlugins[plugin_type]) {
        const installed_version = allInstalledPlugins[plugin_type][plugin_name]['version'];
        const update_available = pluginIsUpgradable(plugin_type, plugin_name, installed_version);
        plugins.push({...allInstalledPlugins[plugin_type][plugin_name], update_available});
      }
    }
    return plugins;
  }

  const pluginIsUpgradable = (pluginType, name, version) => {
    return pluginType in allPlugins && name in allPlugins[pluginType] && semver.gt(allPlugins[pluginType][name].slice(-1)[0]['version'], version);
  }

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
