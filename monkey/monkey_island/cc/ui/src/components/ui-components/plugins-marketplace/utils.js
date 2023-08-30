export const generatePluginId = (plugin) => {
  // Available plugins uses type_, and installed plugins uses plugin_type for
  // the plugin type
  const type = plugin.type_ || plugin.plugin_type;
  return `${plugin.name}${type}${plugin.version}`;
}
