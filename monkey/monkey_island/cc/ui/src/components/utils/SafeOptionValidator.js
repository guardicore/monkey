function getLegacyPluginDescriptors(schema, config) {
  return ([
    {
      name: 'Fingerprinters',
      allPlugins: schema.properties.propagation.properties.network_scan.properties.fingerprinters.items.properties.name.anyOf,
      selectedPlugins: config.propagation.network_scan.fingerprinters
    },
    {
      name: 'CredentialCollectors',
      allPlugins: schema.properties.credential_collectors.items.properties.name.anyOf,
      selectedPlugins: config.credential_collectors
    }
  ]);
}

function getPluginDescriptors(schema, config) {
  return ([
    {
      name: 'Exploiters',
      allPlugins: schema.properties.propagation.properties.exploitation.properties.exploiters.properties,
      selectedPlugins: Object.keys(config.propagation.exploitation.exploiters)
    }
  ])
}

function isUnsafeOptionSelected(schema, config) {
  return isUnsafeLegacyPluginEnabled(schema, config) || isUnsafePluginEnabled(schema, config);
}

function isUnsafeLegacyPluginEnabled(schema, config) {
  let pluginDescriptors = getLegacyPluginDescriptors(schema, config);

  for (let descriptor of pluginDescriptors) {
    if (getUnsafeLegacyPlugins(descriptor).length > 0) {
      return true;
    }
  }

  return false;
}

function getUnsafeLegacyPlugins(pluginDescriptor) {
  let unsafePlugins = [];
  for (let selectedPlugin of pluginDescriptor.selectedPlugins) {
    unsafePlugins = pluginDescriptor.allPlugins.filter(
      (pluginSchema) => pluginSchema.enum[0] === selectedPlugin.name
        && !isPluginSafe(pluginSchema))
  }

  return unsafePlugins;
}

function isUnsafePluginEnabled(schema, config) {
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
