function getFullDefinitionByKey(items, itemKey) {
  let fullArray = items.anyOf;
  return fullArray.filter(e => (e.enum[0] === itemKey))[0];
}

export {getFullDefinitionByKey};
