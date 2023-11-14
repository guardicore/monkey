//eslint-disable-next-line @typescript-eslint/no-var-requires
const next = require('next');

// note the "https" not "http" required module. You will get an error if trying to connect with https
//eslint-disable-next-line @typescript-eslint/no-var-requires
const https = require('https');

//eslint-disable-next-line @typescript-eslint/no-var-requires
const fs = require('fs');
//eslint-disable-next-line no-undef
const port = process.env.HTTPS_PORT || 4430;
//eslint-disable-next-line no-undef
const app = next({
    //eslint-disable-next-line no-undef
    dev: process.env.NODE_ENV !== 'production',
    port: port
});

const sslOptions = {
    key: fs.readFileSync(`./certs/monkey-test.key`),
    cert: fs.readFileSync(`./certs/monkey-test.crt`)
};

const handle = app.getRequestHandler();

app.prepare().then(() => {
    console.log('Starting server...');
    const server = https.createServer(sslOptions, (req, res) => {
        return handle(req, res);
    });
    console.log('Listening on port ' + port);
    server.on('error', (err) => {
        console.error('Error listening on port ' + port + ': ' + err);
        throw err;
    });
    server.listen(port, () => {
        console.log('> Ready on https://localhost:' + port);
    });
});
