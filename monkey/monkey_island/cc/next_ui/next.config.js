/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    env: {},
    compiler: {
        removeConsole: true
    },
    typescript: {
        // !! WARN !!
        // Dangerously allow production builds to successfully complete even if
        // your project has type errors.
        // !! WARN !!
        ignoreBuildErrors: true,
    },
    //async rewrites() {
    //    return [
    //        {
    //            source: '/api/:path*',
    //            destination: 'https://67ba-78-58-178-207.ngrok-free.app/api/:path*',
    //        },
    //    ]
    //},
};

//eslint-disable-next-line no-undef
module.exports = nextConfig;
