const HEADER_SUFFIX = '--header';

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

export const getPluginsGridHeaders = (getRowActions) => [
  {headerName: 'Name', field: 'name', sortable: true, filterable: false, flex: 0.4, minWidth: 150, isTextual: true},
  {headerName: 'Version', field: 'version', sortable: false, filterable: false, flex: 0.1, minWidth: 100, isTextual: true},
  {headerName: 'Type', field: 'type', sortable: true, filterable: false, flex: 0.2, minWidth: 150, isTextual: true},
  {headerName: 'Author', field: 'author', sortable: true, filterable: false, minWidth: 150, flex: 0.25, isTextual: true},
  {headerName: 'Description', field: 'description', sortable: false, filterable: false, minWidth: 150, flex: 1, isTextual: true},
  {
    headerName: '',
    field: 'row_actions',
    type: 'actions',
    minWidth: 100,
    flex: 0.1,
    flexValue: 0.5,
    headerClassName: `row-actions${HEADER_SUFFIX}`,
    cellClassName: `row-actions`,
    getActions: (params) => {
      return getRowActions(params.row);
    }
  }
]

export const getPluginsGridRows = (pluginsList) => {
  const plugins = pluginsList?.map((pluginObject) => {
    const {name, version, type_, author, description} = {...pluginObject};
    return {
      id: generatePluginId(pluginObject),
      name: name,
      version: version,
      type: type_,
      author: author,
      description: description
    }
  })

  return plugins || [];
}

export const extractPluginsPropertyValues = (plugins, fieldToExtract) => {
  const values = [];
  plugins?.forEach((plugin) => {
    if (!values.includes(plugin?.[fieldToExtract]?.trim())) {
      values.push(plugin[fieldToExtract].trim());
    }
  })
  return values.sort();
}
