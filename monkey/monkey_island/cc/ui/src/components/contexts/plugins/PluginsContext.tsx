import React, {createContext, useEffect, useState} from 'react';
import AuthComponent from '../../AuthComponent';
import semver from 'semver';
import _ from 'lodash';

export const PluginsContext = createContext({});

// Types returned from the API
type PluginMetadata = {
  name: string,
  type_: string,
  resource_path: string,
  sha256: string,
  description: string,
  version: string,
  safe: boolean
}

type PluginMetadataResponse = {
  [key: string]: {[key: string]: PluginMetadata[]}
}

type PluginFromManifest = {
  name: string,
  plugin_type: string,
  supported_operating_systems: string[],
  target_operating_systems: string[],
  title: string,
  version: string,
  description: string,
  remediation_suggestion?: string,
  link_to_documentation?: string,
  safe: boolean
}

type PluginManifestResponse = {
  [key: string]: {[key: string]: PluginFromManifest[]}
}

// Types used in the UI
type AgentPlugin = {
  id: string,
  name: string,
  pluginType: string,
  description: string,
  safe: boolean,
  version: string,
}

type InstalledPlugin = AgentPlugin & {
  title: string,
  supportedOperatingSystems: string[],
  targetOperatingSystems: string[],
  linkToDocumentation?: string,
  remediationSuggestion?: string,
}

type AvailablePlugin = AgentPlugin & {
  resourcePath: string,
  sha256: string,
}

export const generatePluginId = (name, type, version) => {
  return `${name}${type}${version}`;
}

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
    refreshNumberOfUpgradablePlugins();
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

  const refreshNumberOfUpgradablePlugins = () => {
    const numUpgradablePlugins = installedPlugins?.filter(plugin => plugin.update_version !== '')?.length;
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
        const update_version = getUpdatedVersion(plugin_type, plugin_name, installed_version);
        plugins.push({...allInstalledPlugins[plugin_type][plugin_name], update_version});
      }
    }
    return plugins;
  }

  const getUpdatedVersion = (pluginType, name, version) => {
    if (pluginIsUpgradable(pluginType, name, version)) {
      return allPlugins[pluginType][name].slice(-1)[0]['version'];
    }
    return '';
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
