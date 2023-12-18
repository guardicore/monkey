// Taken from a server.js that gets generated with "standalone" option
process.env.NODE_ENV = 'production';
process.chdir(__dirname);
// eslint-disable-next-line @typescript-eslint/no-var-requires
const nextConfig = require('./generated-next-config');
process.env.__NEXT_PRIVATE_STANDALONE_CONFIG = JSON.stringify(nextConfig);

const runServer = require('./server-common');
runServer();
