export const reverseObject = (obj) => {
  const reversedObj = {};
  for (const key in obj) {
    const value = obj[key];
    reversedObj[value] = key;
  }
  return reversedObj;
}
