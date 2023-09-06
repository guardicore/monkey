import React, {createContext, useEffect, useState} from 'react';
import semver from 'semver';
import islandHttpClient, {APIEndpoint} from '../../IslandHttpClient';


// Types returned from the API
type PluginMetadata = {
  name: string,
  plugin_type: string,
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
  refreshAvailablePlugins: (force :boolean) => Promise<void>,
  refreshInstalledPlugins: () => Promise<void>,
  refreshNumberOfUpgradablePlugins: () => Promise<void>,
  setInstalledPlugins: (installedPlugins: InstalledPlugin[]) => void,
  setAvailablePlugins: (availablePlugins: AvailablePlugin[]) => void,
  refreshAvailablePluginsFailure: boolean,
  refreshInstalledPluginsFailure: boolean
}

export const PluginsContext = createContext<null | PluginsContextType>(null);

export const generatePluginId = (name, type, version) => {
  return `${name}${type}${version}`;
}


export const PluginState = () :PluginsContextType => {
  const [refreshAvailablePluginsFailure, setRefreshAvailablePluginsFailure] = useState(false);
  const [refreshInstalledPluginsFailure, setRefreshInstalledPluginsFailure] = useState(false);
  const [availablePlugins, setAvailablePlugins] = useState([]);
  const [installedPlugins, setInstalledPlugins] = useState([]);
  const [numberOfPluginsThatRequiresUpdate, setNumberOfPluginsThatRequiresUpdate] = useState(0);


  useEffect(() => {
    refreshInstalledPlugins();
  }, []);

  useEffect(() => {
    refreshAvailablePlugins().then(() => refreshNumberOfUpgradablePlugins());
  }, [installedPlugins]);

  const parsePluginMetadataResponse = (response: PluginMetadataResponse) :AvailablePlugin[] => {
   let plugins :AvailablePlugin[] = [];
    for (const pluginType in response) {
      for (const pluginName in response[pluginType]) {
        let unparsedPlugin = response[pluginType][pluginName].slice(-1)[0];
        let availablePlugin :AvailablePlugin = {
          id: generatePluginId(unparsedPlugin.name, unparsedPlugin.plugin_type, unparsedPlugin.version),
          name: unparsedPlugin.name,
          pluginType: unparsedPlugin.plugin_type,
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

  const handleResponseError = (res: any): void => {
    if (!res || res?.status >= 400) {
      throw new Error();
    }
  }

  const refreshAvailablePlugins = (forceRefresh = false) => {
    let url = APIEndpoint.agentPluginIndex;
    if (forceRefresh) {
      url = APIEndpoint.agentPluginIndexForceRefresh;
    }
    return islandHttpClient.getJSON(url, {}, true)
      .then((res) => { handleResponseError(res); return res; })
      .then((res) => {
        const parsedPlugins = parsePluginMetadataResponse(res.body.plugins);
        setAvailablePlugins(parsedPlugins);
        setRefreshAvailablePluginsFailure(false);
      }).catch(() => {
        setRefreshAvailablePluginsFailure(true);
      })
  };

  const refreshInstalledPlugins = () => {
    return islandHttpClient.getJSON(APIEndpoint.agentPluginManifests, {}, true)
      .then((res) => { handleResponseError(res); return res; })
      .then((resp) => {
        setInstalledPlugins(parsePluginManifestResponse(resp.body));
        setRefreshInstalledPluginsFailure(false);
      }).catch(() => {
        setRefreshInstalledPluginsFailure(true);
      });
  };

  const refreshNumberOfUpgradablePlugins = () => {
    let upgradablePlugins = installedPlugins.filter((installedPlugin) => {
      let availablePlugin = availablePlugins.find((availablePlugin) => {
        return availablePlugin.name === installedPlugin.name
          && availablePlugin.pluginType === installedPlugin.pluginType;
      })
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
    refreshInstalledPlugins,
    refreshAvailablePluginsFailure,
    refreshInstalledPluginsFailure
  }
}
