function getPluginDescriptors(schema, config) {
  return ([
    {
      name: 'Brute force exploiters',
      allPlugins: schema.properties.propagation.properties.exploitation.properties.brute_force.items.anyOf,
      selectedPlugins: config.propagation.exploitation.brute_force
    },
    {
      name: 'Vulnerability exploiters',
      allPlugins: schema.properties.propagation.properties.exploitation.properties.vulnerability.items.anyOf,
      selectedPlugins: config.propagation.exploitation.vulnerability
    },
    {
      name: 'Fingerprinters',
      allPlugins: schema.properties.propagation.properties.network_scan.properties.fingerprinters.items.anyOf,
      selectedPlugins: config.propagation.network_scan.fingerprinters
    },
    {
      name: 'CredentialCollectors',
      allPlugins: schema.properties.credential_collectors.items.anyOf,
      selectedPlugins: config.credential_collectors
    }
  ]);
}

function isUnsafeOptionSelected(schema, config) {
  let pluginDescriptors = getPluginDescriptors(schema, config);

  for (let descriptor of pluginDescriptors) {
    if (isUnsafePluginSelected(descriptor)) {
      return true;
    }
  }

  return false;
}

function isUnsafePluginSelected(pluginDescriptor) {
  let pluginSafety = new Map();
  pluginDescriptor.allPlugins.forEach(i => pluginSafety[i.enum[0]] = i.safe);

  for (let selected of pluginDescriptor.selectedPlugins) {
    if (!pluginSafety[selected.name]) {
      return true;
    }
  }

  return false;
}

export default isUnsafeOptionSelected;
