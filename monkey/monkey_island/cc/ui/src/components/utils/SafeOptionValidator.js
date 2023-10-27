function getLegacyPluginDescriptors(schema, config) {
  return ([
    {
      name: 'Fingerprinters',
      allPlugins: schema.properties.propagation.properties.network_scan.properties.fingerprinters.properties,
      selectedPlugins: Object.keys(config.propagation.network_scan.fingerprinters)
    }
  ]);
}

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
  for (const [name, subschema] of Object.entries(pluginDescriptor.allPlugins)) {
    if (!isPluginSafe(subschema)){
      unsafePlugins.push(name)
    }
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
