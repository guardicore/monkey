require('dotenv').config();
require('dotenv').config({ path: '.env.development', override: true });
process.env.NODE_ENV = 'development';
// eslint-disable-next-line @typescript-eslint/no-var-requires
const runServer = require('./server-common');
runServer();
