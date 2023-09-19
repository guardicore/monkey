export const reverseObject = (obj) => {
  const reversedObj = {};
  for (const key in obj) {
    const value = obj[key];
    reversedObj[value] = key;
  }
  return reversedObj;
}

export const shallowAdditionOfUniqueValueToArray = (arr, value) => {
  const tempArr = [...arr];
  if(!tempArr.includes(value)) {
    tempArr.push(value);
  }
  return tempArr;
}

export const shallowRemovalOfUniqueValueFromArray = (arr, value) => {
  const tempArr = [...arr];
  const indexOfValue = tempArr.indexOf(value);
  if(indexOfValue > -1) {
    tempArr.splice(indexOfValue, 1);
  }
  return tempArr;
}
