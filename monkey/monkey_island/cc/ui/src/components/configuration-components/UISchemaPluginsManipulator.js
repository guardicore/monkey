import MarkdownDescriptionTemplate from './MarkdownDescriptionTemplate';

const RJSF_ATTR_MAPPING = {
  'placeholder': 'ui:placeholder'
};

const pluginsManipulator = (uiSchema, JSONSchema) => {
  for (let pluginName of Object.keys(JSONSchema)) {
    uiSchema[pluginName] = {'ui:DescriptionFieldTemplate': MarkdownDescriptionTemplate, 'ui:readonly': false};
  }

  traversePlugins(uiSchema, JSONSchema);
}

const getObjectByPath = (root, path) => {
    let obj = root
    for (let i = 0; i < path.length; i++) {
      obj = obj[path[i]]
    }
    return obj;
  }

const updateUiSchemaForDynamicComponentsAttributes = (pluginsPaths, uiSchema, JSONSchema) => {
   Object.entries(pluginsPaths).forEach(entry => {
    const [pluginName, paths] = entry;
    // @ts-ignore
    paths?.forEach(path => {
      const pluginObj = getObjectByPath(JSONSchema[pluginName], path);
      Object.entries(pluginObj).forEach(([currField, data]) => {
        Object.keys(data).forEach(attr => {
          if (RJSF_ATTR_MAPPING[attr]) {
            const attrValue = data[attr];
            uiSchema[pluginName] = Object.assign({...uiSchema[pluginName]}, {[currField]: {[RJSF_ATTR_MAPPING[attr]]: attrValue}})
          }
        });
      });
    });
  });
}

const buildPluginsPaths = (JSONSchema) => {
  let pluginsPaths = {};
  for (let pluginName of Object.keys(JSONSchema)) {
    let pluginObject = JSONSchema[pluginName];
    pluginsPaths[pluginName] = getPropertiesPaths(pluginObject, []);
  }

  return pluginsPaths;
}

const getPropertiesPaths = (root, currentPath = []) => {
  const paths = [];

  for (const key in root) {
    const newPath = [...currentPath, key];
    if (key === 'properties') {
      paths.push(...getPropertiesPaths(root[key], newPath));
      if (typeof root[key] === 'object' && root[key] !== null && root[newPath[newPath.length - 1] + 1] === undefined) {
        paths.push(newPath);
      }
    } else if (typeof root[key] === 'object' && root[key] !== null) {
      paths.push(...getPropertiesPaths(root[key], newPath));
    }
  }

  return paths.filter(path => path[0] === 'properties');
}

const traversePlugins = (uiSchema, JSONSchema) => {
  const pluginsPaths = buildPluginsPaths(JSONSchema);
  updateUiSchemaForDynamicComponentsAttributes(pluginsPaths, uiSchema, JSONSchema);
}

export default pluginsManipulator;
