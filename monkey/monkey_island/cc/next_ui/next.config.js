/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    env: {},
    //output: 'standalone',
    compiler: {
        removeConsole:
            process.env.NODE_ENV === process.env.NEXT_PUBLIC_PRODUCTION_KEY
    },
    typescript: {
        // !! WARN !!
        // Dangerously allow production builds to successfully complete even if
        // your project has type errors.
        // !! WARN !!
        ignoreBuildErrors: true
    }
};

//eslint-disable-next-line no-undef
module.exports = nextConfig;
