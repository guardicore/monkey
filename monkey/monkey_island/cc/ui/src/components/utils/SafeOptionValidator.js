function getPluginDescriptors(schema, config) {
  return ([
    {
      name: 'Exploiters',
      allPlugins: schema.properties.propagation.properties.exploitation.properties.exploiters.properties,
      selectedPlugins: Object.keys(config.propagation.exploitation.exploiters)
    },
    {
      name: 'CredentialsCollectors',
      allPlugins: schema.properties.credentials_collectors.properties,
      selectedPlugins: Object.keys(config.credentials_collectors)
    },
    {
      name: 'Payloads',
      allPlugins: schema.properties.payloads.properties,
      selectedPlugins: Object.keys(config.payloads)
    }
  ])
}

function isUnsafeOptionSelected(schema, config) {
  let pluginDescriptors = getPluginDescriptors(schema, config);

  for (let descriptor of pluginDescriptors) {
    if (getUnsafePlugins(descriptor).length > 0) {
      return true;
    }
  }

  return false;
}

function getUnsafePlugins(pluginDescriptor) {
  return pluginDescriptor.selectedPlugins.filter(
    (pluginName) => !isPluginSafe(pluginDescriptor.allPlugins[pluginName]))
}

function isPluginSafe(pluginSchema) {
  return pluginSchema.safe !== undefined && pluginSchema.safe
}

export default isUnsafeOptionSelected;
