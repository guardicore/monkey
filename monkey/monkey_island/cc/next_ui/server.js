const next = require('next');

// note the "https" not "http" required module. You will get an error if trying to connect with https
const https = require('https');

const fs = require('fs');

const config = fs.readFileSync('../server_config.json')
const configJson = JSON.parse(config)
const port = configJson.node_port

const sslOptions = {
    key: fs.readFileSync('../server.key'),
    cert: fs.readFileSync('../server.crt'),
};

const app = next({dev: false, port: port});
const handle = app.getRequestHandler()

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
