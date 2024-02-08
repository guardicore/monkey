import type { NextApiRequest, NextApiResponse } from 'next';
import { createProxyMiddleware } from 'http-proxy-middleware';

const proxyMiddleware = createProxyMiddleware({
    target: 'https://localhost:5000',
    secure: false,
    changeOrigin: true
});

export default function handler(req: NextApiRequest, res: NextApiResponse) {
    // @ts-ignore
    proxyMiddleware(req, res, (result: unknown) => {
        if (result instanceof Error) {
            throw result;
        }
    });
}

export const config = {
    api: {
        externalResolver: true,
        // Uncomment to fix stalled POST requests
        // https://github.com/chimurai/http-proxy-middleware/issues/795#issuecomment-1314464432
        bodyParser: false
    }
};
