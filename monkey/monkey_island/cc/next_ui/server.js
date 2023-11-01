const next = require('next');

// note the "https" not "http" required module. You will get an error if trying to connect with https
const https = require('https');

const fs = require('fs');

const port = process.env.NODE_PORT;
const ssl_cert_path = process.env.SSL_CERT_PATH;
const ssl_key_path = process.env.SSL_KEY_PATH;

const sslOptions = {
    key: fs.readFileSync(ssl_key_path),
    cert: fs.readFileSync(ssl_cert_path)
};

const app = next({dev: false, port: port});
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
