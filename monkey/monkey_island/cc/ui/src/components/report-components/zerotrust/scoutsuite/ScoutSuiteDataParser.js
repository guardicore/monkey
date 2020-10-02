export default class ScoutSuiteDataParser {
  constructor(runResults) {
    this.runResults = runResults
  }

  /*
  itemPath contains path to a specific value e.g. s3.buckets.da1e7081077ce92.secure_transport_enabled"
  templatePath contains a template path for resource we would want to display e.g. s3.buckets.id
   */
  getResourceValue(itemPath, templatePath) {
    let resourcePath = this.fillTemplatePath(itemPath, templatePath);
    return this.getValueAt(resourcePath);
  }

  fillTemplatePath(itemPath, templatePath) {
    let itemPathArray = itemPath.split('.');
    let templatePathArray = templatePath.split('.');
    let resourcePathArray = templatePathArray.map((val, i) => {return val === 'id' ? itemPathArray[i] : val})
    return resourcePathArray.join('.');
  }

  getValueAt(path) {
    return this.getValueAtRecursive(path, this.runResults)
  }

  getValueAtRecursive(path, source) {
    let value = source;
    let current_path = path;
    let key;
    // iterate over each path elements
    while (current_path) {
      // check if there are more elements to the path
      if (current_path.indexOf('.') != -1) {
        key = current_path.substr(0, current_path.indexOf('.'));
      }
      // last element
      else {
        key = current_path;
      }

      try {
        // path containing an ".id"
        if (key == 'id') {
          let v = [];
          let w;
          for (let k in value) {
            // process recursively
            w = this.getValueAtRecursive(k + current_path.substr(current_path.indexOf('.'), current_path.length), value);
            v = v.concat(
              Object.values(w) // get values from array, otherwise it will be an array of key/values
            );
          }
          return v;
        }
        // simple path, just return element in value
        else {
          value = value[key];
        }
      } catch (err) {
        console.log('Error: ' + err)
      }

      // check if there are more elements to process
      if (current_path.indexOf('.') != -1) {
        current_path = current_path.substr(current_path.indexOf('.') + 1, current_path.length);
      }
      // otherwise we're done
      else {
        current_path = false;
      }
    }
    return value;
  }
}
