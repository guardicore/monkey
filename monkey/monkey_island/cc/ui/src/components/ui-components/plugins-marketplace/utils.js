export const pluginsToArray = (plugins) => {
  let pluginsArray = [];
  for (const [type, value] of Object.entries(plugins)) {
    pluginsArray.push(value);
  }
  return pluginsArray;
}

export const generatePluginId = (plugin) => {
  return `${plugin.name}${plugin.type_}${plugin.version}`;
}
