function getPluginDescriptors(schema, config) {
  return ([
    {
      name: 'Exploiters',
      allPlugins: schema.definitions.exploiter_classes.anyOf,
      selectedPlugins: config.basic.exploiters.exploiter_classes
    },
    {
      name: 'Fingerprinters',
      allPlugins: schema.definitions.finger_classes.anyOf,
      selectedPlugins: config.internal.classes.finger_classes
    },
    {
      name: 'PostBreachActions',
      allPlugins: schema.definitions.post_breach_actions.anyOf,
      selectedPlugins: config.monkey.post_breach.post_breach_actions
    },
    {
      name: 'SystemInfoCollectors',
      allPlugins: schema.definitions.system_info_collector_classes.anyOf,
      selectedPlugins: config.monkey.system_info.system_info_collector_classes
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
    if (!pluginSafety[selected]) {
      return true;
    }
  }

  return false;
}

export default isUnsafeOptionSelected;
