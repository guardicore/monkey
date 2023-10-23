const next = require('next')

// note the "https" not "http" required module. You will get an error if trying to connect with https
const https = require('https')
const {parse} = require('url');

const fs = require('fs');
const port = 443
const app = next({dev: false, port: port});

const sslOptions = {
    key: fs.readFileSync('../server.key'),
    cert: fs.readFileSync('../server.crt')
}

const handle = app.getRequestHandler()

app.prepare().then(() => {
    const server = https.createServer(sslOptions, (req, res) => {
        return handle(req, res);
    })
    server.listen(port, (err) => {
        if (err) throw err
        console.log('> Ready on https://localhost:' + port);
    })
})
