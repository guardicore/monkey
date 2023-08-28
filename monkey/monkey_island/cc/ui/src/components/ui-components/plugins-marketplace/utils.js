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
    for (const plugin_name in plugins[plugin_type]) {
      pluginsArray.push(plugins[plugin_type][plugin_name])
    }
  }
  return pluginsArray;
}

export const generatePluginId = (plugin) => {
  // Available plugins uses type_, and installed plugins uses plugin_type for
  // the plugin type
  const type = plugin.type_ || plugin.plugin_type;
  return `${plugin.name}${type}${plugin.version}`;
}
