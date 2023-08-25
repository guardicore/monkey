import {nanoid} from 'nanoid';

const versions = ['1.0.0', '1.1.1', '2.1.3'];
const types = ['exploiter', 'credentials'];
const upgradeableOptions = [true, false];

const generateData = (num, isInstalled = false) => {
  let arr = [];
  for (let i = 0; i < num; i++) {
    const type = types[Math.floor(Math.random() * types.length)];
    const description = `${type} ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum`;
    const obj = {
      id: nanoid(),
      name: `plugin_${i}`,
      version: versions[Math.floor(Math.random() * versions.length)],
      type_: type,
      author: `Monkey Team - ${nanoid()}`,
      description: description
    }
    if (isInstalled) {
      obj['upgradeable'] = upgradeableOptions[Math.floor(Math.random() * upgradeableOptions.length)]
    }
    arr.push(obj);
  }
  return arr;
}

export const getPlugins = (installed = false, shouldResolveEmpty = false, shouldResolve = true) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (shouldResolve) {
        shouldResolveEmpty ? resolve([]) : (installed ? resolve(generateData(20, true)) : resolve(generateData(15)));
      } else {
        reject('Errorrr')
      }
    }, 0);
  })
};

export const installPlugin = (id, success = true) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (success) {
        resolve(id);
      } else {
        reject('Errorrr install')
      }
    }, 5000);
  })
}

export const uninstallPlugin = (id, success = true) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (success) {
        resolve(id);
      } else {
        reject('Errorrr uninstall')
      }
    }, 5000);
  })
}

export const upgradePlugin = (id, success = true) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (success) {
        resolve(id);
      } else {
        reject('Errorrr upgrade')
      }
    }, 5000);
  })
}
