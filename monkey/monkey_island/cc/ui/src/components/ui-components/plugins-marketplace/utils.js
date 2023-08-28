export const pluginIndexToArray = (index) => {
  let pluginsArray = [];
  for (const plugin_type in index) {
    for (const plugin_name in index[plugin_type]) {
      // Only the last version of the plugin is used
      pluginsArray.push(index[plugin_type][plugin_name].slice(-1)[0])
    }
  }
  return pluginsArray;
}

export const installedPluginsToArray = (plugins) => {
  let pluginsArray = [];
  for (const plugin_type in plugins) {
      pluginsArray.push(...plugins[plugin_type])
  }
  return pluginsArray;
}

export const generatePluginId = (plugin) => {
  return `${plugin.name}${plugin.type_}${plugin.version}`;
}
