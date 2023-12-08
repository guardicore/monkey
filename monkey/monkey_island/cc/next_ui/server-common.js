const runServer = () => {
    //eslint-disable-next-line @typescript-eslint/no-var-requires
    const next = require('next');
    // eslint-disable-next-line @typescript-eslint/no-var-requires
    const https = require('https');
    //eslint-disable-next-line @typescript-eslint/no-var-requires
    const fs = require('fs');

    const host = '0.0.0.0';
    const port = process.env.NEXT_PUBLIC_JAVASCRIPT_RUNTIME_PORT;
    const ssl_cert_path = process.env.SSL_CERT_PATH;
    const ssl_key_path = process.env.SSL_KEY_PATH;
    const dev = Boolean(process.env.DEV);

    const sslOptions = {
        key: fs.readFileSync(ssl_key_path),
        cert: fs.readFileSync(ssl_cert_path)
    };

    const app = next({dev: dev, hostname: host, port: port});
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
            console.log(`Ready on https://${host}:${port}`);
        });
    });
};

module.exports = runServer;
