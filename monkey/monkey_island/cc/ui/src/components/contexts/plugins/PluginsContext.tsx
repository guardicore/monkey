import React, {createContext, useEffect, useState} from 'react';
import AuthComponent from '../../AuthComponent';
import semver from 'semver';


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
export type AgentPlugin = {
  id: string,
  name: string,
  pluginType: string,
  description: string,
  safe: boolean,
  version: string,
}

export type InstalledPlugin = AgentPlugin & {
  title: string,
  supportedOperatingSystems: string[],
  targetOperatingSystems: string[],
  linkToDocumentation?: string,
  remediationSuggestion?: string,
}

export type AvailablePlugin = AgentPlugin & {
  resourcePath: string,
  sha256: string,
}

export type PluginsContextType = {
  availablePlugins: AvailablePlugin[],
  installedPlugins: InstalledPlugin[],
  numberOfPluginsThatRequiresUpdate: number,
  refreshAvailablePlugins: () => Promise<void>,
  refreshInstalledPlugins: () => Promise<void>,
  refreshNumberOfUpgradablePlugins: () => Promise<void>,
  setInstalledPlugins: (installedPlugins: InstalledPlugin[]) => void,
  setAvailablePlugins: (availablePlugins: AvailablePlugin[]) => void,
}

export const PluginsContext :null | PluginsContextType  = createContext(null);

export const generatePluginId = (name, type, version) => {
  return `${name}${type}${version}`;
}

const authComponent = new AuthComponent({});

export const PluginState = () :PluginsContextType => {
  const [availablePlugins, setAvailablePlugins] = useState([]);
  const [installedPlugins, setInstalledPlugins] = useState([]);
  const [numberOfPluginsThatRequiresUpdate, setNumberOfPluginsThatRequiresUpdate] = useState(0);


  useEffect(() => {
    refreshInstalledPlugins()
  }, []);

  useEffect(() => {
    refreshAvailablePlugins().then(() => refreshNumberOfUpgradablePlugins())
  }, [installedPlugins]);

  const parsePluginMetadataResponse = (response: PluginMetadataResponse) :AvailablePlugin[] => {
   let plugins :AvailablePlugin[] = [];
    for (const pluginType in response) {
      for (const pluginName in response[pluginType]) {
        let unparsedPlugin = response[pluginType][pluginName].slice(-1)[0];
        let availablePlugin :AvailablePlugin = {
          id: generatePluginId(unparsedPlugin.name, unparsedPlugin.type_, unparsedPlugin.version),
          name: unparsedPlugin.name,
          pluginType: unparsedPlugin.type_,
          description: unparsedPlugin.description,
          safe: unparsedPlugin.safe,
          version: unparsedPlugin.version,
          resourcePath: unparsedPlugin.resource_path,
          sha256: unparsedPlugin.sha256,
        };
        plugins.push(availablePlugin);
      }
    }
    return plugins;
  }

  const parsePluginManifestResponse = (response: PluginManifestResponse) :InstalledPlugin[] => {
    let plugins :InstalledPlugin[] = [];
      for (const pluginType in response) {
        for (const pluginName in response[pluginType]) {
          const installedVersion = response[pluginType][pluginName]['version'];
          const unparsedPlugin = response[pluginType][pluginName];
          let installedPlugin :InstalledPlugin = {
            id: generatePluginId(pluginName, pluginType, installedVersion),
            name: pluginName,
            pluginType: pluginType,
            description: unparsedPlugin['description'],
            safe: unparsedPlugin['safe'],
            version: installedVersion,
            title: unparsedPlugin['title'],
            supportedOperatingSystems: unparsedPlugin['supported_operating_systems'],
            targetOperatingSystems: unparsedPlugin['target_operating_systems'],
            linkToDocumentation: unparsedPlugin['link_to_documentation'],
            remediationSuggestion: unparsedPlugin['remediation_suggestion'],
          }
          plugins.push(installedPlugin);
        }
      }
    return plugins;
  }

  const refreshAvailablePlugins = (forceRefresh = false) => {
    let url = '/api/agent-plugins/available/index';
    if (forceRefresh) {
      url += '?force_refresh=true';
    }
    return authComponent.authFetch(url, {}, true)
      .then(res => res.json())
      .then((res) => {
        let parsedPlugins = parsePluginMetadataResponse(res.plugins);
        setAvailablePlugins(parsedPlugins);
      });
  };

  const refreshInstalledPlugins = () => {
    authComponent.authFetch('/api/agent-plugins/installed/manifests', {}, true)
      .then(res => res.json())
      .then((plugins :PluginManifestResponse) => {
        setInstalledPlugins(parsePluginManifestResponse(plugins));
      });
  };

  const refreshNumberOfUpgradablePlugins = () => {
    let upgradablePlugins = installedPlugins.filter((installedPlugin) => {
      let availablePlugin = availablePlugins.find((availablePlugin) => availablePlugin.id === installedPlugin.id)
      if(availablePlugin){
        return semver.gt(availablePlugin.version, installedPlugin.version);
      } else {
        return false
      }
    })
    setNumberOfPluginsThatRequiresUpdate(upgradablePlugins.length);
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
