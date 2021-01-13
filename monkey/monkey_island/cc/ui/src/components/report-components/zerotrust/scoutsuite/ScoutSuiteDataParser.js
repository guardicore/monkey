export default class ScoutSuiteDataParser {
  constructor(runResults) {
    this.runResults = runResults
  }

  /**
   *
   * @param itemPath contains path to a specific value e.g. s3.buckets.da1e7081077ce92.secure_transport_enabled
   * @param templatePath contains a template path for resource we would want to display e.g. s3.buckets.id
   * @returns {*[]|*}
   */
  getResourceValue(itemPath, templatePath) {
    let resourcePath = this.fillTemplatePath(itemPath, templatePath);
    return this.getObjectValueByPath(resourcePath, this.runResults);
  }

  fillTemplatePath(itemPath, templatePath) {
    let itemPathArray = itemPath.split('.');
    let templatePathArray = templatePath.split('.');
    let resourcePathArray = templatePathArray.map((val, i) => {
      return val === 'id' ? itemPathArray[i] : val
    })
    return resourcePathArray.join('.');
  }

  /**
   * Retrieves value from ScoutSuite data object based on path, provided in the rule
   * @param path E.g. a.id.c.id.e
   * @param source E.g. {a: {b: {c: {d: {e: [{result1: 'result1'}, {result2: 'result2'}]}}}}}
   * @returns {*[]|*} E.g. ['result1', 'result2']
   */
  getObjectValueByPath(path, source) {
    let key;

    while (path) {
      key = this.getNextKeyInPath(path);
      source = this.getValueForKey(key, path, source);
      path = this.trimFirstKey(path);
    }

    return source;
  }

  getNextKeyInPath(path) {
    if (path.indexOf('.') !== -1) {
      return path.substr(0, path.indexOf('.'));
    } else {
      return path;
    }
  }

  /**
   * Returns value from object, based on path and current key
   * @param key E.g. "a"
   * @param path E.g. "a.b.c"
   * @param source E.g. {a: {b: {c: 'result'}}}
   * @returns {[]|*}  E.g. {b: {c: 'result'}}
   */
  getValueForKey(key, path, source) {
    if (key === 'id') {
      return this.getValueByReplacingUnknownKey(path, source);
    } else {
      return source[key];
    }
  }

  /**
   * Gets value from object if first key in path doesn't match source object
   * @param path unknown.b.c
   * @param source {a: {b: {c: [{result:'result'}]}}}
   * @returns {[]} 'result'
   */
  getValueByReplacingUnknownKey(path, source) {
    let value = [];
    for (let key in source) {
      value = this.getObjectValueByPath(this.replaceFirstKey(path, key), source);
      value = value.concat(Object.values(value));
    }
    return value;
  }

  /**
   * Replaces first key in path
   * @param path E.g. "one.two.three"
   * @param replacement E.g. "four"
   * @returns string E.g. "four.two.three"
   */
  replaceFirstKey(path, replacement) {
    return replacement + path.substr(path.indexOf('.'), path.length);
  }

  /**
   * Trims the first key from dot separated path.
   * @param path E.g. "one.two.three"
   * @returns {string|boolean} E.g. "two.three"
   */
  trimFirstKey(path) {
    if (path.indexOf('.') !== -1) {
      return path.substr(path.indexOf('.') + 1, path.length);
    } else {
      return false;
    }
  }


}
