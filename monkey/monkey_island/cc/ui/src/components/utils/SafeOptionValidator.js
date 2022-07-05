function getPluginDescriptors(schema, config) {
  return ([
    {
      name: 'Brute force exploiters',
      allPlugins: schema.definitions.brute_force_classes.anyOf,
      selectedPlugins: config.propagation.exploitation.brute_force
    },
    {
      name: 'Vulnerability exploiters',
      allPlugins: schema.definitions.vulnerability_classes.anyOf,
      selectedPlugins: config.propagation.exploitation.vulnerability
    },
    {
      name: 'Fingerprinters',
      allPlugins: schema.definitions.fingerprinter_classes.anyOf,
      selectedPlugins: config.propagation.network_scan.fingerprinters
    },
    {
      name: 'PostBreachActions',
      allPlugins: schema.definitions.post_breach_actions.anyOf,
      selectedPlugins: config.post_breach_actions
    },
    {
      name: 'CredentialCollectors',
      allPlugins: schema.definitions.credential_collectors_classes.anyOf,
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
