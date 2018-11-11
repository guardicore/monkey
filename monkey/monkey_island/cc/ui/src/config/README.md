# About this folder

This folder holds configuration files for different environments.
You can use it to provide your app with different settings based on the 
current environment, e.g. to configure different API base urls depending on 
whether your setup runs in dev mode or is built for distribution.
You can include the configuration into your code like this:

**ES2015 Modules**

```js
import config from 'config';
```

**Common JS**

Due to Babel6 we need to append `.default`.

```js
let config = require('config').default;
```

**Example**

```javascript
import React from 'react';
import config from 'config';

class MyComponent extends React.Component {
  constructor(props, ctx) {
    super(props, ctx);
    let currentAppEnv = config.appEnv;
  }
}
```
