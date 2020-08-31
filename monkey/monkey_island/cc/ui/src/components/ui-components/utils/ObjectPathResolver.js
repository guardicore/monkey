
// Resolves object's path if it's specified in a dot notation.
// (e.g. params: "firstLevel.secondLevel.property", myObject)
export function resolveObjectPath(pathArray, obj) {
    return pathArray.reduce(function(prev, curr) {
        if(curr === '')
          return prev;
        else
          return prev ? prev[curr] : null;
    }, obj || self)
}
