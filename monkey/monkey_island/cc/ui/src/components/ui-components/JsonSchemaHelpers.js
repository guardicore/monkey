import {resolveObjectPath} from './utils/ObjectPathResolver';

function getFullDefinitionByKey(refString, registry, itemKey) {
  let fullArray = getFullDefinitionsFromRegistry(refString, registry);
  return fullArray.filter(e => (e.enum[0] === itemKey))[0];
}

// Definitions passed to components only contains value and label,
// custom fields like "info" or "links" must be pulled from registry object using this function
function getFullDefinitionsFromRegistry(refString, registry) {
  return getObjectFromRegistryByRef(refString, registry).anyOf;
}

function getObjectFromRegistryByRef(refString, registry) {
  let refArray = refString.replace('#', '').split('/');
  return resolveObjectPath(refArray, registry);
}

export {getFullDefinitionByKey, getObjectFromRegistryByRef};
